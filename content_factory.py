import os
from dotenv import load_dotenv
from pyairtable import Api
from claude_api import generate_outline as claude_generate_outline, write_article_section as claude_write_article_section, generate_meta_description as claude_generate_meta_description

def get_airtable_data():
    load_dotenv()
    api_key = os.getenv("AIRTABLE_API_KEY")
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME")
    api = Api(api_key)
    table = api.table(base_id, table_name)
    return table, table.all()

def create_outlines():
    print("Creating outlines...")
    table, records = get_airtable_data()
    records_needing_outline = [r for r in records if r['fields'].get('Keyword') and not r['fields'].get('Outline')]
    
    if not records_needing_outline:
        print("No records found that need outlines.")
        return

    for record in records_needing_outline:
        keyword = record['fields']['Keyword']
        print(f"\nKeyword: {keyword}")
        print("Generating outline...")
        outline = claude_generate_outline(keyword)
        if outline:
            print("Outline generated successfully.")
            outline_cleaned = '\n'.join(line for line in outline.split('\n') if line.strip())
            table.update(record['id'], {'Outline': outline_cleaned})
            print("Outline saved to Airtable.")
        else:
            print("Failed to generate outline.")
        print("-" * 50)
    
    print(f"\nProcessed {len(records_needing_outline)} record(s) that needed outlines.")

def create_articles():
    print("Creating articles...")
    table, records = get_airtable_data()
    records_needing_article = [r for r in records if r['fields'].get('Outline') and not r['fields'].get('Article')]
    
    if not records_needing_article:
        print("No records found that need articles.")
        return

    for record in records_needing_article:
        keyword = record['fields']['Keyword']
        outline = record['fields']['Outline']
        print(f"\nKeyword: {keyword}")
        
        # Parse the outline to get sections
        sections = [line.strip() for line in outline.split('\n') if line.strip().startswith('##')]
        
        full_article = ""
        for section in sections:
            print(f"Writing section: {section}")
            section_content = claude_write_article_section(keyword, outline, full_article, section)
            if section_content:
                full_article += section_content + "\n\n"
                print("Current full article:")
                print(full_article)
                print("-" * 30)
            else:
                print(f"Failed to generate content for section: {section}")
        
        if full_article:
            print("Article generated successfully.")
            table.update(record['id'], {'Article': full_article.strip()})
            print("Article saved to Airtable.")
        else:
            print("Failed to generate article.")
        print("-" * 50)
    
    print(f"\nProcessed {len(records_needing_article)} record(s) that needed articles.")

def add_meta_descriptions():
    print("Adding meta descriptions...")
    table, records = get_airtable_data()
    records_needing_meta = [r for r in records if r['fields'].get('Article') and not r['fields'].get('Meta Description')]
    
    if not records_needing_meta:
        print("No records found that need meta descriptions.")
        return

    for record in records_needing_meta:
        keyword = record['fields']['Keyword']
        article = record['fields']['Article']
        print(f"\nKeyword: {keyword}")
        print("Generating meta description...")
        meta_description = claude_generate_meta_description(keyword, article)
        if meta_description:
            print("Meta description generated successfully.")
            table.update(record['id'], {'Meta Description': meta_description})
            print("Meta description saved to Airtable.")
        else:
            print("Failed to generate meta description.")
        print("-" * 50)
    
    print(f"\nProcessed {len(records_needing_meta)} record(s) that needed meta descriptions.")

# Add this line at the end of the file to ensure the function is exported
__all__ = ['create_outlines', 'create_articles', 'add_meta_descriptions']
