import os

class base_config(object):
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    mysql_ip = os.getenv('HETTYVERSION_MYSQL_IP', '192.168.99.100');

    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@{0}/hettyversion'.format(mysql_ip);

    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'email@example.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'password')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"HettyVersion" <noreply@example.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

    USER_APP_NAME        = "HettyVersion"

    USER_ENABLE_EMAIL              = True      # Register with Email
    USER_ENABLE_CONFIRM_EMAIL      = os.getenv('HV_CONFIRM_EMAIL', 'True') == 'True'      # Force users to confirm their email

    DEBUG = True