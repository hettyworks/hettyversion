import os

class base_config(object):
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    mysql_ip = os.getenv('HETTYVERSION_MYSQL_IP', '192.168.99.100')
    mysql_password = os.getenv('HETTYVERSION_MYSQL_PASS', 'root')

    SQLALCHEMY_DATABASE_URI = 'mysql://root:{0}@{1}/hettyversion'.format(mysql_password,
                                                                         mysql_ip)

    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'email@example.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'password')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"HettyVersion" <noreply@example.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

    USER_APP_NAME        = "HettyVersion"

    USER_ENABLE_EMAIL              = os.getenv('USER_ENABLE_EMAIL') == 'True'
    USER_ENABLE_CONFIRM_EMAIL      = os.getenv('USER_ENABLE_CONFIRM_EMAIL') == 'True'

    DEBUG = os.getenv('HETTYVERSION_DEBUG') == 'True'
