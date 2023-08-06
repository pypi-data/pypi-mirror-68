from getpass import getpass
import logging
import cmd

from .config import Config


class ConfigCmd(cmd.Cmd):
    intro = 'Set up configuration for site parsing. Type help or ? to list commands.\n'
    prompt = '(config) '
    file = None
    _config = Config()
    log = logging.getLogger(__name__)

    def do_add_recipients(self, arg):
        """
        Add recipient emails separated by space:
        add_recipients email1@mail.org email2@mail.org
        """
        self._config.add_recipients(arg.split())

    def do_remove_recipients(self, arg):
        """Remove listed emails from the recipient list."""
        self._config.remove_recipients(arg.split())

    def do_clear_recipients(self, arg):
        """Clears the recipient list."""
        self._config.clear_recipients()

    def do_set_filename(self, arg):
        """
        Set config filename. The config will be updated if the file exists.
        """
        self._config.set_filename(arg)

    def do_set_server_email(self, arg):
        """Set server email"""
        self._config.set_server_mail(arg)

    def do_set_password(self, arg):
        """Set an admin email password"""

        self._config.set_password(getpass())

    def do_save(self, arg):
        """
        Saves config to the config file.
        """
        self._config.save()

    def do_set_admin_email(self, arg):
        """Set admin email"""
        self._config.set_admin_email(arg)

    def do_show_config(self, arg):
        """Show current config"""
        print(self._config)

    def do_show_password(self, arg):
        """Show password"""
        if input('This is extremely unsafe, do not ever write programs anymore! Y/n ?').lower() in 'y yes'.split():
            print(self._config.password)

    def do_exit(self, arg):
        """
        Exit the program.
        """
        self.log.info('The program is closed by user.')
        return True
