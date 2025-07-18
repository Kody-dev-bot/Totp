locale_messages: dict = {
    "add": {
        "add_success": {
            "en_US": "{0} App added success",
            "zh_CN": "{0} 添加成功"
        },
        "already_exists": {
            "en_US": "{0} App already exists",
            "zh_CN": "{0} 应用已存在"
        },
        "add_failed": {
            "en_US": "{0} App add failed",
            "zh_CN": "{0} 添加失败"
        },
    },
    "delete": {
        "delete_success": {
            "en_US": "{0} App delete success",
            "zh_CN": "{0} 删除成功"
        },
        "delete_failed": {
            "en_US": "{0} App delete failed",
            "zh_CN": "{0} 删除失败"
        },
    },
    "update": {
        "update_success": {
            "en_US": "{0} App update success",
            "zh_CN": "{0} 更新成功"
        },
        "update_failed": {
            "en_US": "{0} App update failed",
            "zh_CN": "{0} 更新失败"
        },
    },
    "app": {
        "app_not_exists": {
            "en_US": "App {0} not exists",
            "zh_CN": "应用 {0} 不存在"
        },
    }
}


import locale

def get_message(nested_key, *args):
    lang = locale.getlocale()[0]
    if not lang:
        lang = "en_US"
    elif lang in ["zh_CN", "Chinese (Simplified)_China"]:
        lang = "zh_CN"
    elif lang in ["en_US", "English_United States"] or lang.startswith("en"):
        lang = "en_US"
    else:
        lang = "en_US"

    # 分割嵌套键
    parts = nested_key.split('.')
    if len(parts) != 2:
        return f"Invalid nested key: {nested_key}"

    category, key = parts
    category_dict = locale_messages.get(category)
    if not category_dict:
        return f"Message not found: {nested_key}"

    message_template = category_dict.get(key)
    if not message_template:
        return f"Message not found: {nested_key}"

    message = message_template.get(lang, message_template.get("en_US"))
    if not message:
        return f"Message not found: {nested_key}"

    try:
        return message.format(*args) if args else message
    except IndexError:
        # 可选：处理参数数量不匹配的情况
        return message  # 或者返回一个错误提示