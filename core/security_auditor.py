import requests
import json
import os
from termcolor import colored

class SecurityAuditor:
    def __init__(self, url, project_dir):
        self.url = url
        self.project_dir = project_dir
        self.report = {
            "url": url,
            "ssl_valid": False,
            "https_enforced": False,
            "security_headers": {},
            "input_vulnerabilities": []
        }

    def run_all_checks(self):
        print(colored(f"🛡️  Starting Security Audit for {self.url}...", "magenta"))
        self.check_ssl_and_https()
        self.check_security_headers()
        self.save_report()
        return self.report

    def check_ssl_and_https(self):
        print(colored("   🔍 Checking SSL & HTTPS...", "white"))
        try:
            # Try with verification first
            response = requests.get(self.url, timeout=10)
            self.report["ssl_valid"] = True
            self.report["https_enforced"] = self.url.startswith("https")
        except requests.exceptions.SSLError:
            print(colored("   ⚠️ SSL Verification Failed (Invalid or Missing CA)", "yellow"))
            self.report["ssl_valid"] = False
            # Try without verification to at least get headers
            try:
                response = requests.get(self.url, timeout=10, verify=False)
                self.report["https_enforced"] = response.url.startswith("https")
            except: pass
        except Exception as e:
            print(colored(f"   ⚠️ SSL Check Failed: {e}", "yellow"))

    def check_security_headers(self):
        print(colored("   🔍 Analyzing Security Headers...", "white"))
        headers_to_check = [
            "Content-Security-Policy",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "Strict-Transport-Security",
            "X-XSS-Protection"
        ]
        try:
            # Use verify=False here to ensure we get headers even if cert is self-signed/invalid
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(self.url, timeout=10, verify=False)
            for header in headers_to_check:
                val = response.headers.get(header)
                self.report["security_headers"][header] = {
                    "present": val is not None,
                    "value": val or "MISSING"
                }
        except Exception as e:
            print(colored(f"   ⚠️ Header Check Failed: {e}", "yellow"))

    def save_report(self):
        output_dir = os.path.join(self.project_dir, "outputs")
        os.makedirs(output_dir, exist_ok=True)
        report_path = os.path.join(output_dir, "security_report.json")
        with open(report_path, "w") as f:
            json.dump(self.report, f, indent=2)
        print(colored(f"✅ Security Report saved: {report_path}", "green"))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python security_auditor.py <URL> <PROJECT_DIR>")
        sys.exit(1)
    
    auditor = SecurityAuditor(sys.argv[1], sys.argv[2])
    auditor.run_all_checks()
