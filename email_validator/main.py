# Требования
# - Принимает список email-адресов
# - Проверяет наличие MX-записей домена
# - Выводит статус для каждого адреса:
#   - "домен валиден"
#   - "домен отсутствует"
#   - "MX-записи отсутствуют или некорректны"

import dns.resolver
import sys

# Парсинг email-адресов (извлечение домена)
def parse_email_addresses(email_addresses: list[str]) -> list[str]:
    domains = []
    for email in email_addresses:
        domains.append(email.split('@')[1])
    return domains

# Обработка исключений (несуществующие домены, отсутствие MX-записей)
def check_email_addresses(domains: list[str]) -> list[str]:
    """
    Проверяет домены и возвращает статусы:
    - "valid" - домен валиден (есть MX-записи)
    - "domain_not_found" - домен отсутствует
    - "no_mx_records" - MX-записи отсутствуют или некорректны
    """
    results = []
    for domain in domains:
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            results.append("valid" if mx_records else "no_mx_records")
        except dns.resolver.NXDOMAIN:
            results.append("domain_not_found")
        except (dns.resolver.NoAnswer, Exception):
            # MX-записей нет, проверяем существование домена через A-запись
            try:
                dns.resolver.resolve(domain, 'A')
                results.append("no_mx_records")
            except dns.resolver.NXDOMAIN:
                results.append("domain_not_found")
            except Exception:
                results.append("no_mx_records")
    return results

# Форматированный вывод результатов
def format_results(domains: list[str], results: list[str]):
    for i in range(len(domains)):
        if results[i] == "valid":
            print(f"домен {domains[i]} валиден")
        elif results[i] == "domain_not_found":
            print(f"домен {domains[i]} отсутствует")
        elif results[i] == "no_mx_records":
            print(f"домен {domains[i]}: MX-записи отсутствуют или некорректны")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        email_addresses = sys.argv[1:]
    else:
        email_addresses = ["test@gmail.com", "test@test.com", "test@nonexistentdomain12345xyz.com"]

    domains = parse_email_addresses(email_addresses)
    results = check_email_addresses(domains)
    format_results(domains, results)