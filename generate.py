from playwright.sync_api import sync_playwright

def generate_client_code(api_endpoints):
    code = '''import requests

class NiceHashAPIClient:
    def __init__(self, api_key: str, api_secret: str, organization_id: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.organization_id = organization_id
        self.base_url = "https://api2.nicehash.com"
    '''

    for endpoint in api_endpoints:
        method_name = endpoint['path'].replace('/', '_').strip('_')
        code += f'''
    def {method_name}(self{", ".join([f", {param}" for param in endpoint['parameters']])}):
        endpoint = "{endpoint['path']}"
        url = self.base_url + endpoint
        headers = {{
            "X-Organization-Id": self.organization_id,
            "X-Api-Key": self.api_key,
        }}
        response = requests.{endpoint['method'].lower()}(url, headers=headers{"".join([f", {param}={param}" for param in endpoint['parameters']])})
        return response.json()
    '''

    return code

def run(playwright) -> None:
    browser = playwright.chromium.launch(headless=True)  # Change to True for headless mode
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://test.nicehash.com/docs/rest")

    api_sections_locator = page.locator(".operation-details")
    api_sections = api_sections_locator.element_handles()

    api_endpoints = []

    for section in api_sections:
        endpoint = {
            'path': section.get_attribute("data-path"),
            'method': section.get_attribute("data-method"),
            'parameters': [param.inner_text() for param in section.locator(".parameter__name")]
        }
        api_endpoints.append(endpoint)

    client_code = generate_client_code(api_endpoints)

    with open('nicehash_api_client.py', 'w') as f:
        f.write(client_code)

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
