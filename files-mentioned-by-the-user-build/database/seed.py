"""Initialize schema and realistic offline demonstration data. Run: flask --app run.py shell < database/seed.py"""
from datetime import datetime, timedelta, date
from app import create_app, db
from app.models import Role, Department, User, Asset, Alert, Incident, Vulnerability, IOC, SecurityLog

app=create_app()
with app.app_context():
    db.create_all()
    if User.query.first(): print("Database already contains data."); raise SystemExit
    roles={"Super Admin":"*","SOC Manager":"alerts.write,alerts.delete,incidents.write,admin","Security Analyst":"alerts.write,incidents.write","Incident Responder":"incidents.write","Auditor":""}
    for name, perms in roles.items(): db.session.add(Role(name=name,permissions=perms))
    for name in ["Security Operations","Infrastructure","Finance","Engineering","Human Resources"]: db.session.add(Department(name=name))
    db.session.flush(); admin=User(username="admin",email="admin@cybershield.local",role=Role.query.filter_by(name="Super Admin").first(),department=Department.query.first()); admin.set_password("ChangeMe!2026"); db.session.add(admin)
    analyst=User(username="analyst",email="analyst@cybershield.local",role=Role.query.filter_by(name="Security Analyst").first()); analyst.set_password("ChangeMe!2026"); db.session.add(analyst)
    db.session.flush()
    assets=[("DC-01","Server","10.0.10.10","Windows Server 2022","Critical","High"),("FIN-WS-22","Workstation","10.0.20.22","Windows 11","High","Medium"),("EDGE-FW-01","Firewall","10.0.0.1","FortiOS","Critical","High"),("ENG-LNX-03","Server","10.0.30.13","Ubuntu 24.04","High","Low")]
    for n,t,ip,os_,c,r in assets: db.session.add(Asset(name=n,asset_type=t,ip_address=ip,operating_system=os_,owner="IT Operations",department=Department.query.first(),criticality=c,risk_level=r,last_scan=datetime.utcnow()))
    db.session.flush(); a=Asset.query.first()
    for title,severity,category,source in [("Ransomware behavioral detection","Critical","Malware","EDR"),("Brute-force authentication attempt","High","Authentication","Active Directory"),("Suspicious PowerShell execution","High","Endpoint","EDR"),("Firewall port scan","Medium","Network","Firewall"),("Phishing email quarantined","Medium","Email","Mail Gateway")]: db.session.add(Alert(title=title,description="Simulated SOC demonstration event requiring analyst review.",severity=severity,status="Open",category=category,source=source,assigned_to=analyst))
    db.session.add(Incident(title="Potential ransomware activity on finance workstation",priority="Critical",status="Investigating",affected_assets="FIN-WS-22",timeline="EDR alert received; host isolated.",investigation_notes="Memory collection requested."))
    db.session.add(Incident(title="Credential stuffing campaign",priority="High",status="Contained",affected_assets="VPN Gateway",timeline="IP blocks deployed.",recovery_steps="Force password resets for affected accounts."))
    for cve,score,desc,risk in [("CVE-2025-12345",9.8,"Critical remote-code-execution exposure","Critical"),("CVE-2024-3094",8.1,"Supply-chain backdoor exposure","High"),("CVE-2024-21762",9.6,"Firewall SSL VPN vulnerability","Critical")]: db.session.add(Vulnerability(cve_id=cve,cvss_score=score,description=desc,risk_level=risk,patch_status="Pending",status="Open",asset=a,remediation_deadline=date.today()+timedelta(days=7)))
    for value,typ,cat,score in [("185.220.101.45","IP","Tor Exit Node",90),("malicious-update.example","Domain","C2",85),("44d88612fea8a8f36de82e1278abb02f","Hash","Malware",95)]: db.session.add(IOC(indicator=value,indicator_type=typ,category=cat,risk_score=score))
    for i in range(30): db.session.add(SecurityLog(log_type="Security",severity="High" if i%7==0 else "Info",source="Windows Event Log",message="Failed login detected" if i%4==0 else "Simulated endpoint telemetry event",event_time=datetime.utcnow()-timedelta(hours=i)))
    db.session.commit(); print("Seeded CyberShield SOC. Login: admin / ChangeMe!2026 (change immediately)")
