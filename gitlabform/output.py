import logging

import cli_ui
import yaml

from gitlabform import EXIT_INVALID_INPUT, EXIT_PROCESSING_ERROR


class EffectiveConfiguration:
    """
    For upgrades and configuration refactoring we want to be able to compare the effective configurations before
    and after the code/app change. This class provides a feature to write the effective configuration into a YAML
    file.
    """

    def __init__(self, output_file):
        if output_file:
            try:
                self.output_file = open(output_file, "w")
                logging.debug(
                    f"Opened file {self.output_file} to write the effective configs to."
                )
            except Exception as e:
                cli_ui.fatal(
                    f"Error when trying to open {self.output_file} to write the effective configs to: {e}",
                    exit_code=EXIT_INVALID_INPUT,
                )
        else:
            self.output_file = None

        self.config = {}

    def add_placeholder(self, project_or_group: str):
        if self.output_file:
            self.config[project_or_group] = {}

    def add_configuration(
        self, project_or_group: str, configuration_name: str, configuration: dict
    ):
        if self.output_file:
            cli_ui.debug(f"Adding effective configuration for {configuration_name}.")
            self.config[project_or_group][configuration_name] = configuration

    def write_to_file(self):
        if self.output_file:
            try:
                yaml_configuration = yaml.dump(
                    self.config,
                    default_flow_style=False,
                )
                self.output_file.write(yaml_configuration)
                self.output_file.close()
            except Exception as e:
                cli_ui.fatal(
                    f"Error when trying to write or close {self.output_file}: {e}",
                    exit_code=EXIT_PROCESSING_ERROR,
                )
