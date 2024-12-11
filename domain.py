def add_to_hosts(domain: str, ip: str):
    """Adiciona um domínio ao arquivo /etc/hosts."""
    try:
        with open('/etc/hosts', encoding='utf-8') as f:
            if domain in f.read():
                return

        with open('/etc/hosts', 'a', encoding='utf-8') as f:
            f.write(f'\n{ip} {domain}')

        print(f'O domínio {domain} foi adicionado ao arquivo /etc/hosts.')
    except PermissionError:
        print('Você precisa de permissão de administrador para executar esta ação.')


add_to_hosts('shura.bb.com.br', '127.0.0.1')
