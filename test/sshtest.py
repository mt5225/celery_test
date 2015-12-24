import spur
import spur.ssh

shell = spur.SshShell(
    hostname="uinnova.com",
    port=22,
    username="ubuntu",
    private_key_file="/Users/mt5225/pem/website_en.pem",
    missing_host_key=spur.ssh.MissingHostKey.accept
    )
with shell:
    result = shell.run(["df", "-h"])
    print result.output
