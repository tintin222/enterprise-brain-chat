#!/usr/bin/env python3
# Enterprise Brain: put the product name into the English strings of the web app and the server. Run it from the
# repository root on upstream's files after moving to a new Mattermost release; running it again changes nothing.
#   python3 enterprise-brain/rebrand_strings.py
# "Mattermost" stays where a string means Mattermost's own software, company, services or licences.
import json
import re
from pathlib import Path

WEBAPP = Path("webapp/channels/src/i18n/en.json")
SERVER = Path("server/i18n/en.json")
NEW = "Enterprise Brain"

# Web app strings outside the System Console.
USER_SKIP = ("admin.", "admin_", "cloud", "license", "trial", "workspace_limits", "self_hosted", "feature_discovery", "pricing", "purchase",
             "billing", "upgrade", "learn_more", "post_priority", "adldap_upsell", "announcement_bar", "feature_restricted_modal",
             "commercial_support", "start_trial", "contact_sales", "deprecation", "notify_admin", "about.copyright", "about.planNameLearn",
             "about.enterprise", "about.licensed", "mobile.", "air_gapped")
USER_KEEP = (r",? Inc|\s(?:Agents|Desktop|desktop|Mobile|mobile|Enterprise|Professional|Entry|\{planName\}|community|Cloud|Marketplace|Boards|"
             r"Playbooks|Calls|Copilot|AI|Academy|Forum|Support|Sales|handbook|documentation|docs)\b")
# System Console strings, except licensing and upsell pages (hidden or unused on this build).
ADMIN_SKIP = ("admin.license", "admin.billing", "admin.trial", "admin.cloud", "admin.subscription", "admin.purchase", "admin.upgrade",
              "admin.workspace_limits", "admin.ldap_feature_discovery", "admin.saml_feature_discovery", "admin.feature_discovery",
              "admin.sidebar.license", "admin.true_up", "admin.self_hosted")
ADMIN_KEEP = (r",? Inc|\s(?:Enterprise|Professional|Entry|Free|Cloud|Hosted|Software|Acceptable|iOS|Android|Mobile|mobile|Desktop|desktop|Apps|"
              r"apps|Agents|Marketplace|Push|Translation|Customer|Support|Sales|community|docs|documentation|handbook|Academy|Forum|license|plans|"
              r"\{planName\}|Team Edition|Boards|Playbooks|Calls|Copilot|AI)\b|\sApps\"")
WEBAPP_OVERRIDES = {
    "about.notice": "Enterprise Brain is built on Mattermost, which is made possible by the open source software used in its <linkServer>server</linkServer>, <linkDesktop>desktop</linkDesktop> and <linkMobile>mobile</linkMobile> apps.",
    "about.teamEditiont0": "Enterprise Brain",
    "about.teamEditionSt": "Team chat with AI agents that know your company.",
    "about.teamEditionLearn": "Built on Mattermost. Source code (AGPL v3): ",
}
# New web app strings: key -> (insert after this key, text).
WEBAPP_NEW = {"web.footer.source": ("web.footer.privacy", "Source code")}

# Server strings people see: emails and slash command help.
SERVER_REPLACE = {
    "api.command.invite_people.desc", "api.command_help.desc", "api.command_logout.desc",
    "api.email_batching.send_batched_email_notification.button", "api.templates.guest_magic_link_body.footer.info",
    "api.templates.guest_magic_link_body.title", "api.templates.invite_body.subTitle", "api.templates.invite_body_footer.title",
    "api.templates.post_body.button", "api.templates.verify_body.info", "api.templates.welcome_body.info",
    "app.notification.footer.infoLogin", "web.error.unsupported_browser.no_longer_support",
    "web.error.unsupported_browser.no_longer_support_version",
}
SERVER_OVERRIDES = {
    "api.templates.email_footer_v2": "© {{ .CurrentYear }} Enterprise Brain",
    "api.templates.invite_body_footer.info": "Enterprise Brain is team chat with AI agents that know your company, built on the open source Mattermost platform.",
}
SERVER_NEW = [{"id": "api.upgrade_to_enterprise.enterprise_brain.app_error", "translation": "This server runs Enterprise Brain chat, which cannot be upgraded to Mattermost Enterprise Edition."}]


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def rebrand_webapp():
    strings = json.loads(WEBAPP.read_text())
    user = re.compile(rf"Mattermost(?!{USER_KEEP})")
    admin = re.compile(rf"Mattermost(?!{ADMIN_KEEP})")
    changed = 0
    for key, text in strings.items():
        if key in WEBAPP_OVERRIDES:
            new = WEBAPP_OVERRIDES[key]
        elif "Mattermost" not in text:
            continue
        elif key.startswith(("admin.", "admin_")):
            new = text if key.startswith(ADMIN_SKIP) else admin.sub(NEW, text)
        else:
            new = text if key.startswith(USER_SKIP) else user.sub(NEW, text)
        if new != text:
            strings[key] = new
            changed += 1
    for key, (after, text) in WEBAPP_NEW.items():
        if key not in strings:
            out = {}
            for k, v in strings.items():
                out[k] = v
                if k == after:
                    out[key] = text
            strings = out if key in out else {**strings, key: text}
            changed += 1
    write_json(WEBAPP, strings)
    return changed


def rebrand_server():
    strings = json.loads(SERVER.read_text())
    changed = 0
    for entry in strings:
        old = entry["translation"]
        if entry["id"] in SERVER_OVERRIDES:
            entry["translation"] = SERVER_OVERRIDES[entry["id"]]
        elif entry["id"] in SERVER_REPLACE:
            entry["translation"] = old.replace("Mattermost", NEW)
        elif entry["id"] == "api.command_help.success" and old.startswith("Mattermost is an open source platform"):
            entry["translation"] = old.replace("Mattermost is an open source platform", "Enterprise Brain is built on Mattermost, an open source platform", 1)
        changed += entry["translation"] != old
    ids = {entry["id"] for entry in strings}
    for new in SERVER_NEW:
        if new["id"] not in ids:
            position = next((i for i, entry in enumerate(strings) if entry["id"] > new["id"]), len(strings))
            strings.insert(position, new)
            changed += 1
    write_json(SERVER, strings)
    return changed


if __name__ == "__main__":
    print(f"web app: {rebrand_webapp()} strings changed; server: {rebrand_server()} strings changed")
