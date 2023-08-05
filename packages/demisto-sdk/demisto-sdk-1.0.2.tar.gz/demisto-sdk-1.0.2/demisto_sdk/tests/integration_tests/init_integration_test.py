import json
from os import listdir
from pathlib import Path

from click.testing import CliRunner
from demisto_sdk.__main__ import main

INIT_CMD = "init"


def test_integration_init_integration_positive(tmp_path):
    """
    Given
    - Inputs to init pack with integration.

    When
    - Running the init command.

    Then
    - Ensure pack metadata is created successfully.
    - Ensure integration directory contain all files.
    """
    pack_name = "SuperPack"
    fill_pack_metadata = "Y"
    pack_display_name = "SuperPackDisplayName"
    pack_desc = "This is a super pack desc"
    support_type = "1"
    pack_author = "SuperMario"
    pack_url = "https://www.github.com/supermario"
    pack_email = "mario@super.com"
    pack_category = "4"
    pack_tags = "SuperTag1,SuperTag2"
    create_integration = 'Y'
    integration_name = "SuperIntegration"
    use_dir_name_as_id = 'Y'
    inputs = [pack_name, fill_pack_metadata, pack_display_name, pack_desc, support_type,
              pack_author, pack_url, pack_email, pack_category, pack_tags, create_integration, integration_name,
              use_dir_name_as_id]

    d = tmp_path / 'TestPacks'
    d.mkdir()
    tmp_dir_path = Path(d)
    tmp_pack_path = tmp_dir_path / pack_name
    tmp_pack_metadata_path = tmp_pack_path / 'pack_metadata.json'
    tmp_integration_path = tmp_pack_path / 'Integrations' / integration_name

    runner = CliRunner(mix_stderr=False)
    result = runner.invoke(main, [INIT_CMD, '-o', tmp_dir_path], input='\n'.join(inputs))

    assert result.exit_code == 0
    assert f"Successfully created the pack SuperPack in: {tmp_pack_path}" in result.stdout
    assert f"Created pack metadata at path : {tmp_pack_metadata_path}" in result.stdout
    assert f"Finished creating integration: {tmp_integration_path}." in result.stdout
    assert result.stderr == ""

    with open(tmp_pack_metadata_path, 'r') as f:
        metadata_json = json.loads(f.read())
        assert {
            "name": pack_display_name,
            "description": pack_desc,
            "support": "demisto",
            "currentVersion": "1.0.0",
            "author": pack_author,
            "url": pack_url,
            "email": pack_email,
            "categories": [
                "Endpoint"
            ],
            "tags": pack_tags.split(","),
            "beta": False,
            "deprecated": False,
            "useCases": [],
            "keywords": [],
            "dependencies": {}
        }.items() <= metadata_json.items()  # testing for subset (<=) to avoid testing created and modified timestamps

    integration_dir_files = {file for file in listdir(tmp_integration_path)}
    assert {
        "CHANGELOG.md", "Pipfile", "Pipfile.lock", "README.md", f"{integration_name}.py",
        f"{integration_name}.yml", f"{integration_name}_description.md", f"{integration_name}_test.py",
        f"{integration_name}_image.png"
    } == integration_dir_files
