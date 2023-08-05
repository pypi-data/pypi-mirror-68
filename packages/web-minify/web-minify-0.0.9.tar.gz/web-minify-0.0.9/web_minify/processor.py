import os
import pprint
import datetime
import time
from .handlers import html_minify, css_minify, js_minify, sass_minify, png_minify, jpeg_minify, svg_minify
from .files import path_is_in_path, generate_file_list, determine_file_extension
from .time import human_delta
import logging

logger = logging.getLogger(__name__)

now = datetime.datetime.now()


class Processor:
    def __init__(self, settings: dict):
        self.settings = settings
        self.input = settings.get("input", None)
        self.output = settings.get("output", None)
        self.input_is_dir = self.input and os.path.isdir(self.input)
        self.input_exists = self.input and os.path.exists(self.input)
        self.output_is_dir = self.output and os.path.isdir(self.output)
        self.output_exists = self.output and os.path.exists(self.output)

        self.overwrite: bool = settings.get("overwrite", False)
        self.on_change: bool = settings.get("on_change", False)
        self.format: bool = settings.get("format", False)
        self.prefix: bool = settings.get("prefix", False)
        self.zipy: bool = settings.get("zipy", False)
        self.hash: bool = settings.get("hash", False)
        self.verbose: bool = settings.get("verbose", False)
        self.force: bool = settings.get("force", False)

        # fmt off
        self.processor_map = {
            "sass": (sass_minify, False),
            "css": (css_minify, False),
            "html": (html_minify, False),
            "svg": (svg_minify, False),
            "js": (js_minify, False),
            "png": (png_minify, True),
            "jpeg": (jpeg_minify, True)
        }
        # fmt on

        self.valid_extensions = [f".{ext}" for ext in self.processor_map.keys()]
        if self.verbose:
            logger.info("### Settings:")
            logger.info(pprint.pformat(self.settings))
            logger.info("### Valid extensions:")
            logger.info(pprint.pformat(self.valid_extensions))
        self.pool = None

    def sanity_checks(self):
        if not self.input or not self.input_exists:
            return (False, f"The input specified '{self.input}' did not exist. Input must be an existing directory or file")
        if not self.overwrite and self.on_change:
            return (False, f"On-change will not have an effect so long as overwrite is not enabled")
        if not self.output and not self.overwrite and not self.format:
            return (False, f"Only input '{self.input}' was specified. Without a setting for 'output', 'overwrite' and/or 'format' all processing will fail")
        if path_is_in_path(self.input, self.output):
            return (False, f"The output '{self.output}' is a subpath of input '{self.input}'")
        if path_is_in_path(self.output, self.input):
            return (False, f"The input '{self.input}' is a subpath of output '{self.output}'")
        return True, None

    def process_file(self, input_path: str, output_path: str):
        if self.verbose:
            logger.info(f"Processing '{input_path}' to '{output_path}'")
        if not input_path:
            return False, False, False, "No input path specified"
        if not output_path:
            return False, False, False, "No output path specified"
        input_mtime = now.timestamp()
        if os.path.isfile(output_path):
            if not self.overwrite:
                return False, False, False, "Trying to overwrite without overwrite enabled"
            if self.on_change:
                input_mtime = os.path.getmtime(input_path)
                output_mtime = os.path.getmtime(output_path)
                if not self.force and (input_mtime == output_mtime):
                    return True, False, True, "File not changed, skipping"
                elif not self.force and (output_mtime > input_mtime):
                    return True, False, True, "Destination file newer than input, skipping"
        else:
            output_dir = os.path.dirname(output_path)
            if not os.path.isdir(output_dir):
                os.makedirs(name=output_dir, exist_ok=True)
            if not os.path.isdir(output_dir):
                return False, False, False, "Output directory did not exist or could not be created"
        extension = determine_file_extension(input_path)
        if not extension:
            return False, False, False, f"Unknown extension '{extension}' for input file"
        processor, is_binary = self.processor_map.get(extension, None)
        if not processor:
            return False, False, False, "Could not find processor for input file"
        original_content = None
        try:
            with open(input_path, "rb") if is_binary else open(input_path, "r", encoding="utf-8") as file:
                original_content = file.read()
        except Exception as err:
            return False, False, False, f"Could not load data from input file: {err}"
        if not original_content:
            logger.warning(f"Input file '{input_path}' was empty")
        processed_content = None
        was_copied = False
        if extension in ["js", "css", "html", "svg", "png", "jpeg"] and self.settings.get(f"disable_{extension}", False):
            # Perform copy
            # logger.info(f"SUPPOSED TO COPY: {input_path} ({extension})")
            processed_content = original_content
            was_copied = True
        else:
            # logger.info(f"SUPPOSED TO PROCESS: {input_path} ({extension})")
            processed_content = processor(original_content, self.settings)
            # TODO: make message mechanism for processor
        # logger.info(f"Content of file {input_path} was of type {type(original_content)} while processed {type(processed_content)}")
        if None == processed_content:
            logger.warning(f"Processed file for '{input_path}' was empty")
        try:
            with open(output_path, "wb") if is_binary else open(output_path, "w", encoding="utf-8") as file:
                written = file.write(processed_content)
                if written != len(processed_content):
                    return False, False, False, f"Partially written output ({written} of {len(processed_content)} bytes)"
        except Exception as err:
            return False, False, False, f"Could not write data to output file: {err}"
        try:
            os.utime(output_path, (input_mtime, input_mtime))
        except Exception as err:
            return False, False, False, f"Could not modify date of output file: {err}"
        # All went well, go home happy!
        return True, was_copied, False, None

    def process_files_list(self, list):
        start_time = datetime.datetime.now()
        success_count = 0
        copied_count = 0
        skipped_count = 0
        messages = {}
        # logger.info(f'Spreading workload over {multiprocessing.cpu_count()} CPU cores')
        # self.pool = multiprocessing.Pool(multiprocessing.cpu_count())
        for item in list:
            input_path = item["input_path"]
            output_path = item["output_path"]
            single_start_time = datetime.datetime.now()
            success, copied, skipped, message = self.process_file(input_path=input_path, output_path=output_path)
            if success:
                success_count += 1
            if copied:
                copied_count += 1
            if skipped:
                skipped_count += 1
            if message:
                messages[message] = 1 + messages.get(message, 0)

            single_end_time = datetime.datetime.now()
            single_interval = single_end_time - single_start_time
            if single_interval > datetime.timedelta(seconds=1):
                logger.warning(f"Processing of {input_path} was slow ({human_delta(single_interval)})")
        # self.pool.close()
        # self.pool.join()
        # self.pool=None
        end_time = datetime.datetime.now()
        interval = end_time - start_time
        failed = len(list) - success_count
        logger.info(f"Processing of {len(list)} files with {success_count} successful, {copied_count} copied and {skipped_count} skipped, generated {len(messages)} message(s) and took {human_delta(interval)} total")
        if messages:
            logger.warning(f"Messages encountered were:")
            for message, count in messages.items():
                logger.warning(f"{count} x {message}")
        return True

    def _process_existing_dir_to_existing_dir(self):
        input_paths = generate_file_list(self.input, tuple(self.valid_extensions))
        # logger.info(pprint.pformat(input_paths))
        list = []
        for input_path in input_paths:
            common = os.path.commonpath((os.path.abspath(self.output), os.path.abspath(input_path)))
            rel = os.path.relpath(os.path.abspath(input_path), os.path.abspath(self.input))
            output_path = os.path.join(os.path.abspath(self.output), rel)
            list.append({"input_path": input_path, "output_path": output_path})
        # logger.info(pprint.pformat(list))
        return list

    def _process_existing_dir_to_new_dir(self):
        # This is same as _process_existing_dir_to_existing_dir but with a mkdir first
        os.mkdir(self.output)
        self.output_exists = self.output and os.path.exists(self.output)
        return self._process_existing_dir_to_existing_dir()

    def process_files(self):
        if self.input_is_dir:
            if self.output:
                if self.output_is_dir:
                    if self.verbose:
                        logger.info(f"existing-dir-to-existing-dir easy peasy case")
                    list = self._process_existing_dir_to_existing_dir()
                    return self.process_files_list(list)
                elif not self.output_exists:
                    if self.verbose or True:
                        logger.info(f"existing-dir-to-new-dir easy peasy case")
                    list = self._process_existing_dir_to_new_dir()
                    return self.process_files_list(list)
                else:
                    logger.error(f"existing-dir-to-existing-file error")
                    return False
                return False
            elif self.overwite:
                return False
            elif self.format:
                return False
            else:
                logger.error(f"input dir specified without valid output option")
                return False
        else:
            if self.output:
                if self.output_is_dir:
                    if self.verbose or True:
                        logger.info(f"existing-file-to-existing-dir easy peasy case NOT IMPLEMENTED YET!")
                    return False
                elif not self.output_exists:
                    if self.verbose or True:
                        logger.info(f"existing-file-to-new-file easy peasy case NOT IMPLEMENTED YET!")
                    return False
                else:
                    if self.overwite:
                        if self.verbose or True:
                            logger.info(f"existing-file-to-existing-file overwrite easy peasy case NOT IMPLEMENTED YET!")
                        return False
                    else:
                        logger.error(f"existing-file-to-existing-file non-overwrite error")
                        return False
                return False
            elif self.overwite:
                return False
            elif self.format:
                return False
            else:
                logger.error(f"input file specified without valid output option")
                return False
