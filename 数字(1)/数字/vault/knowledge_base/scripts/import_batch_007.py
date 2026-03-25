import json, chromadb, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('../..')

client = chromadb.PersistentClient(path='knowledge_base/vector_store')
col = client.get_collection('refined_abc')
print(f'导入前: {col.count()} 条')

with open('knowledge_base/batch_data/batch_007.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ids = [item['id'] for item in data]
docs = [item['text'] for item in data]
metas = []
for item in data:
    m = {
        'category': item['type'],
        'tags': item['label'],
        'source_file': item['source'],
        'line_numbers': str(item.get('source_lines', '')),
        'confidence': item.get('confidence', ''),
        'review_status': '通过',
        'review_date': '2026-03-23'
    }
    if 'decision_date' in item:
        m['decision_date'] = item['decision_date']
    if 'still_valid' in item:
        m['still_valid'] = str(item['still_valid'])
    metas.append(m)

col.add(ids=ids, documents=docs, metadatas=metas)
print(f'导入后: {col.count()} 条')
print(f'本批: {len(ids)} 条')
for i in ids:
    print(f'  {i}')
