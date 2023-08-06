import subprocess
import sys


def check_translations(
    root_path,
    package_name,
    locales=frozenset(['es']),
    ignored_strings=frozenset(),
):
    # extract messages through to catalogs
    setup_py = str(root_path / 'setup.py')
    subprocess.run(['python', setup_py, 'extract_messages'])
    subprocess.run(['python', setup_py, 'update_catalog', '--no-fuzzy-matching'])
    subprocess.run(['python', setup_py, 'compile_catalog'])
    subprocess.run(['python', setup_py, 'compile_json'])

    found_fuzzy = False
    untranslated_strings = []

    # check for fuzzy matches
    for locale in locales:
        po_path = (
            root_path / package_name / 'i18n' / locale / 'LC_MESSAGES'
            / '{}.po'.format(package_name)
        )
        with open(po_path, mode='rb') as fp:
            contents = fp.read()
            found_fuzzy = found_fuzzy or b'#, fuzzy' in contents

            fp.seek(0)
            from babel.messages.pofile import read_po
            load_catalog = read_po(fp)
            for message in load_catalog:
                if message.id in ignored_strings:
                    continue
                if message.id and not message.string:
                    untranslated_strings.append('{}: {}'.format(locale, message.id))

    # note: the strings below are intentionally left untranslated
    if found_fuzzy:
        print('Detected fuzzy translations.')

    if untranslated_strings:
        print('Did not find translations for the following strings:')
        for item in untranslated_strings:
            print('    ', item)

    if found_fuzzy or untranslated_strings:
        print('Edit the PO file and compile the catalogs.')
        sys.exit(1)

    print('No detected translation issues.')
