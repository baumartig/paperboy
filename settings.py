class Settings:

    def __init__(self):
        self.smtpServer = {}

    def useSmtp(self):
        if len(self.smtpServer):
            return True
        else:
            return False

    def setCalibreFolder(self, folder):
        self.calibreFolder = folder

    def deleteSmtpSettings(self):
        self.smtpServer.clear()

    def setSmtpServer(self, address, port, security):
        self.setSmtpServerAdress(address)

        if port:
            self.setSmtpServerPort(port)
        if security:
            self.setSmtpServerSecurity(security)

    def setSmtpServerAdress(self, address):
        self.smtpServer["address"]=address

    def setSmtpServerPort(self, port):
        self.smtpServer["port"]=int(port)

    def setSmtpServerSecurity(self, security):
        self.smtpServer["security"]=security

    def setSmtpLogin(self, account):
        self.smtpServer["login"]=account

    def setSmtpPassword(self, password):
        self.smtpServer["password"]=password

    def setMailFrom(self, mailFrom):
        self.mailFrom = mailFrom

    def setMailTo(self, mailTo):
        self.mailTo = mailTo

    def setFormat(self, format):
        self.format = format