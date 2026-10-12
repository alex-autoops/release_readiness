import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def show(value):
    print(json.dumps(value, indent=2) if not isinstance(value, str) else value)

def review():
    for name,p in json.loads((ROOT/'release-plan.json').read_text()).items():
        checks={
          'healthy_capacity':p['replicas']-p['batch_size']>=p['minimum_healthy'],
          'failed_health_blocks_release':p['health_check_passed'] or not p['proceed'],
          'correct_endpoint':p['sdk_endpoint']==p['expected_endpoint'],
          'https':p['sdk_endpoint'].startswith('https://'),
          'tls_verification':p['verify_tls'],
          'scoped_role':p['role']=='deployment_only',
          'short_lived_credentials':p['credential_source']=='short_lived_identity'}
        show({'plan':name,'checks':checks,'decision':'ACCEPT' if all(checks.values()) else 'REJECT'})

if __name__ == "__main__":
    review()
