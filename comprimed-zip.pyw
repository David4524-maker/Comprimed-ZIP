# -*- coding: utf-8 -*-
"""
Comprimed-ZIP 1.0
Un compresor de archivos gratuito
David© - Comprimed-ZIP 2026

Ejecuta este archivo en IDLE (Python 3.14) -> F5
"""

import os
import re
import csv
import sys
import json
import zlib
import hmac
import struct
import shutil
import hashlib
import zipfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser, simpledialog

try:
    from PIL import Image
    HAS_PIL = True
except Exception:
    HAS_PIL = False

APP_NAME = "Comprimed-ZIP"
APP_VERSION = "1.0"
CZIP_MAGIC = b"CZIP"
CZIP_VERSION = 1

# ---------------------------------------------------------------------------
# IDIOMAS
# ---------------------------------------------------------------------------
LANGUAGES = [
    "Español", "English", "Français", "Deutsch", "Italiano",
    "Português", "Русский", "中文", "日本語", "العربية",
]

TRANSLATIONS = {
    "Español": {
        "compress_tab": "Comprimir", "convert_tab": "Convertir",
        "czip_tab": "Archivo .czip", "settings_tab": "Ajustes",
        "about_tab": "Acerca de",
        "input": "Archivo de entrada", "output": "Archivo de salida",
        "browse": "Examinar...", "compress_btn": "Comprimir",
        "extract_btn": "Descomprimir", "convert_btn": "Convertir",
        "password": "Contraseña", "level": "Nivel de compresión (0-9)",
        "language": "Idioma", "style": "Estilo",
        "font_size": "Tamaño de fuente", "accent": "Color de acento",
        "choose_color": "Elegir color...",
        "file_menu": "Archivo", "tools_menu": "Herramientas",
        "view_menu": "Ver", "help_menu": "Ayuda",
        "exit": "Salir", "export_html": "Exportar HTML",
        "reset": "Restablecer", "about": "Acerca de",
        "ready": "Listo", "done": "Operación completada",
        "error": "Error", "success": "Éxito",
        "select_file": "Selecciona un archivo",
        "select_output": "Selecciona el archivo de salida",
        "select_czip": "Selecciona un archivo .czip",
        "save_as": "Guardar como...", "open_file": "Abrir archivo",
        "enter_password": "Introduce una contraseña para el .czip",
        "wrong_password": "Contraseña incorrecta o archivo dañado",
        "compressed_msg": "Archivo comprimido correctamente.\nOriginal: {orig} bytes\nFinal: {final} bytes",
        "converted_msg": "Archivo convertido correctamente.",
        "extracted_msg": "Archivo descomprimido correctamente.",
        "target_format": "Formato de destino", "detected": "Formato detectado",
        "czip_compress": "Comprimir a .czip", "czip_extract": "Extraer .czip",
        "about_body": "# Comprimed-ZIP\n\nUn compresor de archivos gratuito\n\nVersion: 1.0\n\nIdioma: {lang}\n\n> David© - Comprimed-ZIP  2026",
    },
    "English": {
        "compress_tab": "Compress", "convert_tab": "Convert",
        "czip_tab": ".czip File", "settings_tab": "Settings",
        "about_tab": "About",
        "input": "Input file", "output": "Output file",
        "browse": "Browse...", "compress_btn": "Compress",
        "extract_btn": "Extract", "convert_btn": "Convert",
        "password": "Password", "level": "Compression level (0-9)",
        "language": "Language", "style": "Style",
        "font_size": "Font size", "accent": "Accent color",
        "choose_color": "Choose color...",
        "file_menu": "File", "tools_menu": "Tools",
        "view_menu": "View", "help_menu": "Help",
        "exit": "Exit", "export_html": "Export HTML",
        "reset": "Reset", "about": "About",
        "ready": "Ready", "done": "Operation completed",
        "error": "Error", "success": "Success",
        "select_file": "Select a file",
        "select_output": "Select the output file",
        "select_czip": "Select a .czip file",
        "save_as": "Save as...", "open_file": "Open file",
        "enter_password": "Enter a password for the .czip file",
        "wrong_password": "Wrong password or corrupted file",
        "compressed_msg": "File compressed successfully.\nOriginal: {orig} bytes\nFinal: {final} bytes",
        "converted_msg": "File converted successfully.",
        "extracted_msg": "File extracted successfully.",
        "target_format": "Target format", "detected": "Detected format",
        "czip_compress": "Compress to .czip", "czip_extract": "Extract .czip",
        "about_body": "# Comprimed-ZIP\n\nA free file compressor\n\nVersion: 1.0\n\nLanguage: {lang}\n\n> David© - Comprimed-ZIP  2026",
    },
    "Français": {
        "compress_tab": "Compresser", "convert_tab": "Convertir",
        "czip_tab": "Fichier .czip", "settings_tab": "Paramètres",
        "about_tab": "À propos",
        "input": "Fichier d'entrée", "output": "Fichier de sortie",
        "browse": "Parcourir...", "compress_btn": "Compresser",
        "extract_btn": "Extraire", "convert_btn": "Convertir",
        "password": "Mot de passe", "level": "Niveau de compression (0-9)",
        "language": "Langue", "style": "Style",
        "font_size": "Taille de police", "accent": "Couleur d'accent",
        "choose_color": "Choisir une couleur...",
        "file_menu": "Fichier", "tools_menu": "Outils",
        "view_menu": "Affichage", "help_menu": "Aide",
        "exit": "Quitter", "export_html": "Exporter HTML",
        "reset": "Réinitialiser", "about": "À propos",
        "ready": "Prêt", "done": "Opération terminée",
        "error": "Erreur", "success": "Succès",
        "select_file": "Sélectionnez un fichier",
        "select_output": "Sélectionnez le fichier de sortie",
        "select_czip": "Sélectionnez un fichier .czip",
        "save_as": "Enregistrer sous...", "open_file": "Ouvrir un fichier",
        "enter_password": "Entrez un mot de passe pour le .czip",
        "wrong_password": "Mot de passe incorrect ou fichier corrompu",
        "compressed_msg": "Fichier compressé avec succès.\nOriginal : {orig} octets\nFinal : {final} octets",
        "converted_msg": "Fichier converti avec succès.",
        "extracted_msg": "Fichier extrait avec succès.",
        "target_format": "Format cible", "detected": "Format détecté",
        "czip_compress": "Compresser en .czip", "czip_extract": "Extraire .czip",
        "about_body": "# Comprimed-ZIP\n\nUn compresseur de fichiers gratuit\n\nVersion: 1.0\n\nLangue : {lang}\n\n> David© - Comprimed-ZIP  2026",
    },
    "Deutsch": {
        "compress_tab": "Komprimieren", "convert_tab": "Konvertieren",
        "czip_tab": ".czip-Datei", "settings_tab": "Einstellungen",
        "about_tab": "Über",
        "input": "Eingabedatei", "output": "Ausgabedatei",
        "browse": "Durchsuchen...", "compress_btn": "Komprimieren",
        "extract_btn": "Extrahieren", "convert_btn": "Konvertieren",
        "password": "Passwort", "level": "Komprimierungsstufe (0-9)",
        "language": "Sprache", "style": "Stil",
        "font_size": "Schriftgröße", "accent": "Akzentfarbe",
        "choose_color": "Farbe wählen...",
        "file_menu": "Datei", "tools_menu": "Werkzeuge",
        "view_menu": "Ansicht", "help_menu": "Hilfe",
        "exit": "Beenden", "export_html": "HTML exportieren",
        "reset": "Zurücksetzen", "about": "Über",
        "ready": "Bereit", "done": "Vorgang abgeschlossen",
        "error": "Fehler", "success": "Erfolg",
        "select_file": "Datei auswählen",
        "select_output": "Ausgabedatei auswählen",
        "select_czip": ".czip-Datei auswählen",
        "save_as": "Speichern unter...", "open_file": "Datei öffnen",
        "enter_password": "Passwort für die .czip-Datei eingeben",
        "wrong_password": "Falsches Passwort oder beschädigte Datei",
        "compressed_msg": "Datei erfolgreich komprimiert.\nOriginal: {orig} Bytes\nEndgröße: {final} Bytes",
        "converted_msg": "Datei erfolgreich konvertiert.",
        "extracted_msg": "Datei erfolgreich extrahiert.",
        "target_format": "Zielformat", "detected": "Erkanntes Format",
        "czip_compress": "In .czip komprimieren", "czip_extract": ".czip extrahieren",
        "about_body": "# Comprimed-ZIP\n\nEin kostenloser Dateikompressor\n\nVersion: 1.0\n\nSprache: {lang}\n\n> David© - Comprimed-ZIP  2026",
    },
    "Italiano": {
        "compress_tab": "Comprimi", "convert_tab": "Converti",
        "czip_tab": "File .czip", "settings_tab": "Impostazioni",
        "about_tab": "Informazioni",
        "input": "File di input", "output": "File di output",
        "browse": "Sfoglia...", "compress_btn": "Comprimi",
        "extract_btn": "Estrai", "convert_btn": "Converti",
        "password": "Password", "level": "Livello di compressione (0-9)",
        "language": "Lingua", "style": "Stile",
        "font_size": "Dimensione carattere", "accent": "Colore accento",
        "choose_color": "Scegli colore...",
        "file_menu": "File", "tools_menu": "Strumenti",
        "view_menu": "Visualizza", "help_menu": "Aiuto",
        "exit": "Esci", "export_html": "Esporta HTML",
        "reset": "Ripristina", "about": "Informazioni",
        "ready": "Pronto", "done": "Operazione completata",
        "error": "Errore", "success": "Successo",
        "select_file": "Seleziona un file",
        "select_output": "Seleziona il file di output",
        "select_czip": "Seleziona un file .czip",
        "save_as": "Salva come...", "open_file": "Apri file",
        "enter_password": "Inserisci una password per il .czip",
        "wrong_password": "Password errata o file danneggiato",
        "compressed_msg": "File compresso con successo.\nOriginale: {orig} byte\nFinale: {final} byte",
        "converted_msg": "File convertito con successo.",
        "extracted_msg": "File estratto con successo.",
        "target_format": "Formato di destinazione", "detected": "Formato rilevato",
        "czip_compress": "Comprimi in .czip", "czip_extract": "Estrai .czip",
        "about_body": "# Comprimed-ZIP\n\nUn compressore di file gratuito\n\nVersion: 1.0\n\nLingua: {lang}\n\n> David© - Comprimed-ZIP  2026",
    },
    "Português": {
        "compress_tab": "Comprimir", "convert_tab": "Converter",
        "czip_tab": "Arquivo .czip", "settings_tab": "Configurações",
        "about_tab": "Sobre",
        "input": "Arquivo de entrada", "output": "Arquivo de saída",
        "browse": "Procurar...", "compress_btn": "Comprimir",
        "extract_btn": "Extrair", "convert_btn": "Converter",
        "password": "Senha", "level": "Nível de compressão (0-9)",
        "language": "Idioma", "style": "Estilo",
        "font_size": "Tamanho da fonte", "accent": "Cor de destaque",
        "choose_color": "Escolher cor...",
        "file_menu": "Arquivo", "tools_menu": "Ferramentas",
        "view_menu": "Exibir", "help_menu": "Ajuda",
        "exit": "Sair", "export_html": "Exportar HTML",
        "reset": "Redefinir", "about": "Sobre",
        "ready": "Pronto", "done": "Operação concluída",
        "error": "Erro", "success": "Sucesso",
        "select_file": "Selecione um arquivo",
        "select_output": "Selecione o arquivo de saída",
        "select_czip": "Selecione um arquivo .czip",
        "save_as": "Salvar como...", "open_file": "Abrir arquivo",
        "enter_password": "Digite uma senha para o .czip",
        "wrong_password": "Senha incorreta ou arquivo corrompido",
        "compressed_msg": "Arquivo comprimido com sucesso.\nOriginal: {orig} bytes\nFinal: {final} bytes",
        "converted_msg": "Arquivo convertido com sucesso.",
        "extracted_msg": "Arquivo extraído com sucesso.",
        "target_format": "Formato de destino", "detected": "Formato detectado",
        "czip_compress": "Comprimir para .czip", "czip_extract": "Extrair .czip",
        "about_body": "# Comprimed-ZIP\n\nUm compressor de arquivos gratuito\n\nVersion: 1.0\n\nIdioma: {lang}\n\n> David© - Comprimed-ZIP  2026",
    },
    "Русский": {
        "compress_tab": "Сжать", "convert_tab": "Конвертировать",
        "czip_tab": "Файл .czip", "settings_tab": "Настройки",
        "about_tab": "О программе",
        "input": "Входной файл", "output": "Выходной файл",
        "browse": "Обзор...", "compress_btn": "Сжать",
        "extract_btn": "Извлечь", "convert_btn": "Конвертировать",
        "password": "Пароль", "level": "Уровень сжатия (0-9)",
        "language": "Язык", "style": "Стиль",
        "font_size": "Размер шрифта", "accent": "Акцентный цвет",
        "choose_color": "Выбрать цвет...",
        "file_menu": "Файл", "tools_menu": "Инструменты",
        "view_menu": "Вид", "help_menu": "Справка",
        "exit": "Выход", "export_html": "Экспорт HTML",
        "reset": "Сброс", "about": "О программе",
        "ready": "Готово", "done": "Операция завершена",
        "error": "Ошибка", "success": "Успех",
        "select_file": "Выберите файл",
        "select_output": "Выберите выходной файл",
        "select_czip": "Выберите файл .czip",
        "save_as": "Сохранить как...", "open_file": "Открыть файл",
        "enter_password": "Введите пароль для .czip",
        "wrong_password": "Неверный пароль или повреждённый файл",
        "compressed_msg": "Файл успешно сжат.\nОригинал: {orig} байт\nИтог: {final} байт",
        "converted_msg": "Файл успешно конвертирован.",
        "extracted_msg": "Файл успешно извлечён.",
        "target_format": "Целевой формат", "detected": "Обнаруженный формат",
        "czip_compress": "Сжать в .czip", "czip_extract": "Извлечь .czip",
        "about_body": "# Comprimed-ZIP\n\nБесплатный компрессор файлов\n\nVersion: 1.0\n\nЯзык: {lang}\n\n> David© - Comprimed-ZIP  2026",
    },
    "中文": {
        "compress_tab": "压缩", "convert_tab": "转换",
        "czip_tab": ".czip 文件", "settings_tab": "设置",
        "about_tab": "关于",
        "input": "输入文件", "output": "输出文件",
        "browse": "浏览...", "compress_btn": "压缩",
        "extract_btn": "解压", "convert_btn": "转换",
        "password": "密码", "level": "压缩级别 (0-9)",
        "language": "语言", "style": "风格",
        "font_size": "字体大小", "accent": "强调色",
        "choose_color": "选择颜色...",
        "file_menu": "文件", "tools_menu": "工具",
        "view_menu": "视图", "help_menu": "帮助",
        "exit": "退出", "export_html": "导出 HTML",
        "reset": "重置", "about": "关于",
        "ready": "就绪", "done": "操作完成",
        "error": "错误", "success": "成功",
        "select_file": "选择文件",
        "select_output": "选择输出文件",
        "select_czip": "选择 .czip 文件",
        "save_as": "另存为...", "open_file": "打开文件",
        "enter_password": "输入 .czip 文件的密码",
        "wrong_password": "密码错误或文件损坏",
        "compressed_msg": "文件压缩成功。\n原始大小：{orig} 字节\n压缩后：{final} 字节",
        "converted_msg": "文件转换成功。",
        "extracted_msg": "文件解压成功。",
        "target_format": "目标格式", "detected": "检测到的格式",
        "czip_compress": "压缩为 .czip", "czip_extract": "解压 .czip",
        "about_body": "# Comprimed-ZIP\n\n免费文件压缩器\n\nVersion: 1.0\n\n语言: {lang}\n\n> David© - Comprimed-ZIP  2026",
    },
    "日本語": {
        "compress_tab": "圧縮", "convert_tab": "変換",
        "czip_tab": ".czip ファイル", "settings_tab": "設定",
        "about_tab": "情報",
        "input": "入力ファイル", "output": "出力ファイル",
        "browse": "参照...", "compress_btn": "圧縮",
        "extract_btn": "展開", "convert_btn": "変換",
        "password": "パスワード", "level": "圧縮レベル (0-9)",
        "language": "言語", "style": "スタイル",
        "font_size": "フォントサイズ", "accent": "アクセントカラー",
        "choose_color": "色を選択...",
        "file_menu": "ファイル", "tools_menu": "ツール",
        "view_menu": "表示", "help_menu": "ヘルプ",
        "exit": "終了", "export_html": "HTML をエクスポート",
        "reset": "リセット", "about": "情報",
        "ready": "準備完了", "done": "操作が完了しました",
        "error": "エラー", "success": "成功",
        "select_file": "ファイルを選択",
        "select_output": "出力ファイルを選択",
        "select_czip": ".czip ファイルを選択",
        "save_as": "名前を付けて保存...", "open_file": "ファイルを開く",
        "enter_password": ".czip のパスワードを入力",
        "wrong_password": "パスワードが違うか、ファイルが破損しています",
        "compressed_msg": "ファイルを正常に圧縮しました。\n元のサイズ: {orig} バイト\n最終サイズ: {final} バイト",
        "converted_msg": "ファイルを正常に変換しました。",
        "extracted_msg": "ファイルを正常に展開しました。",
        "target_format": "変換先の形式", "detected": "検出された形式",
        "czip_compress": ".czip に圧縮", "czip_extract": ".czip を展開",
        "about_body": "# Comprimed-ZIP\n\n無料のファイル圧縮ツール\n\nVersion: 1.0\n\n言語: {lang}\n\n> David© - Comprimed-ZIP  2026",
    },
    "العربية": {
        "compress_tab": "ضغط", "convert_tab": "تحويل",
        "czip_tab": "ملف .czip", "settings_tab": "الإعدادات",
        "about_tab": "حول",
        "input": "ملف الإدخال", "output": "ملف الإخراج",
        "browse": "استعراض...", "compress_btn": "ضغط",
        "extract_btn": "استخراج", "convert_btn": "تحويل",
        "password": "كلمة المرور", "level": "مستوى الضغط (0-9)",
        "language": "اللغة", "style": "النمط",
        "font_size": "حجم الخط", "accent": "لون التمييز",
        "choose_color": "اختر اللون...",
        "file_menu": "ملف", "tools_menu": "أدوات",
        "view_menu": "عرض", "help_menu": "مساعدة",
        "exit": "خروج", "export_html": "تصدير HTML",
        "reset": "إعادة تعيين", "about": "حول",
        "ready": "جاهز", "done": "اكتملت العملية",
        "error": "خطأ", "success": "نجاح",
        "select_file": "اختر ملفًا",
        "select_output": "اختر ملف الإخراج",
        "select_czip": "اختر ملف .czip",
        "save_as": "حفظ باسم...", "open_file": "فتح ملف",
        "enter_password": "أدخل كلمة مرور لملف .czip",
        "wrong_password": "كلمة مرور خاطئة أو ملف تالف",
        "compressed_msg": "تم ضغط الملف بنجاح.\nالأصلي: {orig} بايت\nالنهائي: {final} بايت",
        "converted_msg": "تم تحويل الملف بنجاح.",
        "extracted_msg": "تم استخراج الملف بنجاح.",
        "target_format": "التنسيق الهدف", "detected": "التنسيق المكتشف",
        "czip_compress": "ضغط إلى .czip", "czip_extract": "استخراج .czip",
        "about_body": "# Comprimed-ZIP\n\nضاغط ملفات مجاني\n\nVersion: 1.0\n\nاللغة: {lang}\n\n> David© - Comprimed-ZIP  2026",
    },
}

# ---------------------------------------------------------------------------
# ESTILOS
# ---------------------------------------------------------------------------
STYLES = {
    "Comprimed-ZIP": {
        "bg": "#1e1e2e", "fg": "#cdd6f4",
        "accent": "#89b4fa", "accent_fg": "#11111b",
        "button_bg": "#313244", "entry_bg": "#181825", "entry_fg": "#cdd6f4",
        "button_relief": "flat", "button_bd": 0,
    },
    "WinRAR": {
        "bg": "#d4d0c8", "fg": "#000000",
        "accent": "#0a246a", "accent_fg": "#ffffff",
        "button_bg": "#e6e3db", "entry_bg": "#ffffff", "entry_fg": "#000000",
        "button_relief": "raised", "button_bd": 2,
    },
    "7-Zip": {
        "bg": "#f0f0f0", "fg": "#202020",
        "accent": "#3a7bc8", "accent_fg": "#ffffff",
        "button_bg": "#e6e6e6", "entry_bg": "#ffffff", "entry_fg": "#000000",
        "button_relief": "raised", "button_bd": 1,
    },
}

# ---------------------------------------------------------------------------
# CONVERSIONES
# ---------------------------------------------------------------------------
CONVERSIONS = {
    ".txt":  [".md", ".html", ".json"],
    ".md":   [".txt", ".html"],
    ".csv":  [".json"],
    ".json": [".csv", ".txt"],
    ".html": [".txt"],
    ".png":  [".jpg", ".bmp", ".webp"],
    ".jpg":  [".png", ".bmp", ".webp"],
    ".jpeg": [".png", ".bmp", ".webp"],
    ".bmp":  [".png", ".jpg", ".webp"],
    ".webp": [".png", ".jpg", ".bmp"],
}

# ---------------------------------------------------------------------------
# .CZIP — Cifrado propio
# ---------------------------------------------------------------------------
def _derive_key(password: str, salt: bytes, length: int = 32) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000, dklen=length)

def _xor_stream(data: bytes, key: bytes, nonce: bytes) -> bytes:
    out = bytearray(len(data))
    counter = 0
    offset = 0
    while offset < len(data):
        block = hashlib.sha256(key + nonce + counter.to_bytes(8, "big")).digest()
        chunk = min(len(block), len(data) - offset)
        for i in range(chunk):
            out[offset + i] = data[offset + i] ^ block[i]
        offset += chunk
        counter += 1
    return bytes(out)

def write_czip(src_path: str, dst_path: str, password: str, level: int = 9) -> None:
    with open(src_path, "rb") as f:
        raw = f.read()
    comp = zlib.compress(raw, level)
    salt = os.urandom(16)
    nonce = os.urandom(16)
    key = _derive_key(password, salt, 32)
    mac_key = _derive_key(password + "|mac", salt, 32)
    enc = _xor_stream(comp, key, nonce)
    tag = hmac.new(mac_key, salt + nonce + enc, hashlib.sha256).digest()
    header = CZIP_MAGIC + bytes([CZIP_VERSION]) + salt + nonce + struct.pack(">Q", len(raw))
    with open(dst_path, "wb") as f:
        f.write(header)
        f.write(enc)
        f.write(tag)

def read_czip(src_path: str, dst_path: str, password: str) -> None:
    with open(src_path, "rb") as f:
        data = f.read()
    if not data.startswith(CZIP_MAGIC):
        raise ValueError("Not a .czip file")
    pos = 4
    version = data[pos]; pos += 1
    if version != CZIP_VERSION:
        raise ValueError("Unsupported .czip version")
    salt = data[pos:pos+16]; pos += 16
    nonce = data[pos:pos+16]; pos += 16
    pos += 8  # original length (reservado)
    tag = data[-32:]
    enc = data[pos:-32]
    key = _derive_key(password, salt, 32)
    mac_key = _derive_key(password + "|mac", salt, 32)
    expected = hmac.new(mac_key, salt + nonce + enc, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expected):
        raise ValueError("Wrong password or corrupted file")
    comp = _xor_stream(enc, key, nonce)
    raw = zlib.decompress(comp)
    with open(dst_path, "wb") as f:
        f.write(raw)

# ---------------------------------------------------------------------------
# CONVERTIDOR
# ---------------------------------------------------------------------------
def _escape_html(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def convert_file(src: str, dst_ext: str, out_path: str) -> None:
    src_ext = os.path.splitext(src)[1].lower()
    dst_ext = dst_ext.lower()
    if not dst_ext.startswith("."):
        dst_ext = "." + dst_ext

    if src_ext in (".txt", ".md", ".html") and dst_ext in (".txt", ".md", ".html", ".json"):
        with open(src, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        if dst_ext == ".html":
            out = ("<!DOCTYPE html><html><head><meta charset='utf-8'>"
                   "<title>Converted by Comprimed-ZIP</title></head>"
                   "<body><pre>" + _escape_html(text) + "</pre></body></html>")
        elif dst_ext == ".json":
            out = json.dumps({"content": text}, ensure_ascii=False, indent=2)
        elif dst_ext == ".txt" and src_ext == ".html":
            out = re.sub(r"<[^>]+>", "", text)
        else:
            out = text
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(out)
        return

    if src_ext == ".csv" and dst_ext == ".json":
        with open(src, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        return

    if src_ext == ".json" and dst_ext == ".csv":
        with open(src, encoding="utf-8") as f:
            data = json.load(f)
        if not (isinstance(data, list) and data and isinstance(data[0], dict)):
            raise ValueError("JSON must be a list of objects")
        keys = list(data[0].keys())
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(data)
        return

    if HAS_PIL and src_ext in (".png", ".jpg", ".jpeg", ".bmp", ".webp") \
            and dst_ext in (".png", ".jpg", ".jpeg", ".bmp", ".webp"):
        img = Image.open(src)
        if dst_ext in (".jpg", ".jpeg") and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(out_path)
        return

    # Fallback: copia binaria
    shutil.copy2(src, out_path)

# ---------------------------------------------------------------------------
# APP
# ---------------------------------------------------------------------------
class ComprimedZIP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} {APP_VERSION}")
        self.geometry("900x640")
        self.minsize(780, 560)

        self.language = "Español"
        self.style_name = "Comprimed-ZIP"
        self.font_size = 10
        self.custom_accent = None

        self._init_vars()
        self._build_body()
        self._build_menu()
        self.apply_style()
        self.retranslate()
        self.set_status("ready")

    # ------- helpers -------
    def t(self, key, **kw):
        lang = getattr(self, "language", "English")
        val = TRANSLATIONS.get(lang, {}).get(key)
        if val is None:
            val = TRANSLATIONS["English"].get(key, key)
        if kw:
            try:
                return val.format(**kw)
            except Exception:
                return val
        return val

    def set_status(self, key, **kw):
        self.var_status.set(self.t(key, **kw))

    # ------- variables -------
    def _init_vars(self):
        self.var_compress_in = tk.StringVar()
        self.var_compress_out = tk.StringVar()
        self.var_compress_level = tk.IntVar(value=9)
        self.var_convert_in = tk.StringVar()
        self.var_convert_out = tk.StringVar()
        self.var_convert_target = tk.StringVar()
        self.var_convert_detected = tk.StringVar(value="-")
        self.var_czip_in = tk.StringVar()
        self.var_czip_out = tk.StringVar()
        self.var_czip_pwd = tk.StringVar()
        self.var_status = tk.StringVar()
        self.var_language = tk.StringVar(value=self.language)
        self.var_style = tk.StringVar(value=self.style_name)
        self.var_font = tk.StringVar(value=str(self.font_size))

    # ------- menú -------
    def _build_menu(self):
        if hasattr(self, "menubar"):
            try:
                self.config(menu="")
                self.menubar.destroy()
            except Exception:
                pass
        self.menubar = tk.Menu(self)
        t = self.t

        m_file = tk.Menu(self.menubar, tearoff=0)
        m_file.add_command(label=t("compress_btn"), command=lambda: self.notebook.select(0))
        m_file.add_command(label=t("convert_btn"), command=lambda: self.notebook.select(1))
        m_file.add_separator()
        m_file.add_command(label=t("export_html"), command=self.export_html)
        m_file.add_separator()
        m_file.add_command(label=t("exit"), command=self.destroy)
        self.menubar.add_cascade(label=t("file_menu"), menu=m_file)

        m_tools = tk.Menu(self.menubar, tearoff=0)
        m_tools.add_command(label=t("czip_tab"), command=lambda: self.notebook.select(2))
        self.menubar.add_cascade(label=t("tools_menu"), menu=m_tools)

        m_view = tk.Menu(self.menubar, tearoff=0)
        m_view.add_command(label=t("settings_tab"), command=lambda: self.notebook.select(3))
        self.menubar.add_cascade(label=t("view_menu"), menu=m_view)

        m_help = tk.Menu(self.menubar, tearoff=0)
        m_help.add_command(label=t("about_tab"), command=lambda: self.notebook.select(4))
        self.menubar.add_cascade(label=t("help_menu"), menu=m_help)

        self.config(menu=self.menubar)

    # ------- cuerpo -------
    def _build_body(self):
        self.header = tk.Frame(self)
        self.header.pack(fill="x", padx=12, pady=(10, 4))
        self.lbl_title = tk.Label(self.header, text=APP_NAME)
        self.lbl_title.pack(side="left")
        self.lbl_version = tk.Label(self.header, text=f"v{APP_VERSION}")
        self.lbl_version.pack(side="left", padx=(8, 0), pady=(6, 0))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(0, 6))

        self.tab_compress = tk.Frame(self.notebook)
        self.tab_convert = tk.Frame(self.notebook)
        self.tab_czip = tk.Frame(self.notebook)
        self.tab_settings = tk.Frame(self.notebook)
        self.tab_about = tk.Frame(self.notebook)

        for tab in (self.tab_compress, self.tab_convert, self.tab_czip,
                    self.tab_settings, self.tab_about):
            self.notebook.add(tab, text="")

        self._build_compress_tab()
        self._build_convert_tab()
        self._build_czip_tab()
        self._build_settings_tab()
        self._build_about_tab()

        self.status = tk.Label(self, textvariable=self.var_status, anchor="w", padx=12)
        self.status.pack(fill="x")

    def _file_row(self, parent, label_attr, var, browse_cmd):
        row = tk.Frame(parent)
        row.pack(fill="x", padx=12, pady=6)
        row.columnconfigure(0, weight=1)
        lbl = tk.Label(row, text="")
        lbl.grid(row=0, column=0, sticky="w")
        ent = tk.Entry(row, textvariable=var)
        ent.grid(row=1, column=0, sticky="we", padx=(0, 6))
        btn = tk.Button(row, command=browse_cmd)
        btn.grid(row=1, column=1)
        setattr(self, label_attr, lbl)
        return lbl, ent, btn

    def _build_compress_tab(self):
        f = self.tab_compress
        self.lbl_c_in, self.ent_c_in, self.btn_c_in = self._file_row(f, "lbl_c_in", self.var_compress_in, self.pick_compress_in)
        self.lbl_c_out, self.ent_c_out, self.btn_c_out = self._file_row(f, "lbl_c_out", self.var_compress_out, self.pick_compress_out)

        row = tk.Frame(f)
        row.pack(fill="x", padx=12, pady=6)
        self.lbl_c_level = tk.Label(row, text="")
        self.lbl_c_level.pack(side="left")
        self.spin_c_level = tk.Spinbox(row, from_=0, to=9, width=4, textvariable=self.var_compress_level)
        self.spin_c_level.pack(side="left", padx=8)

        btns = tk.Frame(f)
        btns.pack(fill="x", padx=12, pady=12)
        self.btn_compress = tk.Button(btns, command=self.do_compress)
        self.btn_compress.pack(side="left")
        self.btn_extract_zip = tk.Button(btns, command=self.do_extract_zip)
        self.btn_extract_zip.pack(side="left", padx=8)

    def _build_convert_tab(self):
        f = self.tab_convert
        self.lbl_v_in, self.ent_v_in, self.btn_v_in = self._file_row(f, "lbl_v_in", self.var_convert_in, self.pick_convert_in)

        row = tk.Frame(f)
        row.pack(fill="x", padx=12, pady=6)
        self.lbl_v_detected = tk.Label(row, text="")
        self.lbl_v_detected.pack(side="left")
        self.lbl_v_detected_val = tk.Label(row, textvariable=self.var_convert_detected)
        self.lbl_v_detected_val.pack(side="left", padx=(4, 16))

        self.lbl_v_target = tk.Label(row, text="")
        self.lbl_v_target.pack(side="left")
        self.opt_convert_target = tk.OptionMenu(row, self.var_convert_target, "")
        self.opt_convert_target.pack(side="left", padx=8)

        self.lbl_v_out, self.ent_v_out, self.btn_v_out = self._file_row(f, "lbl_v_out", self.var_convert_out, self.pick_convert_out)

        btns = tk.Frame(f)
        btns.pack(fill="x", padx=12, pady=12)
        self.btn_convert = tk.Button(btns, command=self.do_convert)
        self.btn_convert.pack(side="left")

    def _build_czip_tab(self):
        f = self.tab_czip
        self.lbl_z_in, self.ent_z_in, self.btn_z_in = self._file_row(f, "lbl_z_in", self.var_czip_in, self.pick_czip_in)
        self.lbl_z_out, self.ent_z_out, self.btn_z_out = self._file_row(f, "lbl_z_out", self.var_czip_out, self.pick_czip_out)

        row = tk.Frame(f)
        row.pack(fill="x", padx=12, pady=6)
        self.lbl_z_pwd = tk.Label(row, text="")
        self.lbl_z_pwd.pack(side="left")
        self.ent_z_pwd = tk.Entry(row, textvariable=self.var_czip_pwd, show="•", width=30)
        self.ent_z_pwd.pack(side="left", padx=8)

        btns = tk.Frame(f)
        btns.pack(fill="x", padx=12, pady=12)
        self.btn_czip_compress = tk.Button(btns, command=self.do_czip_compress)
        self.btn_czip_compress.pack(side="left")
        self.btn_czip_extract = tk.Button(btns, command=self.do_czip_extract)
        self.btn_czip_extract.pack(side="left", padx=8)

    def _build_settings_tab(self):
        f = self.tab_settings
        row = tk.Frame(f); row.pack(fill="x", padx=12, pady=8)
        self.lbl_s_lang = tk.Label(row, text=""); self.lbl_s_lang.pack(side="left")
        self.opt_lang = tk.OptionMenu(row, self.var_language, *LANGUAGES, command=self._on_language_change)
        self.opt_lang.pack(side="left", padx=8)

        row = tk.Frame(f); row.pack(fill="x", padx=12, pady=8)
        self.lbl_s_style = tk.Label(row, text=""); self.lbl_s_style.pack(side="left")
        self.opt_style = tk.OptionMenu(row, self.var_style, *STYLES.keys(), command=self._on_style_change)
        self.opt_style.pack(side="left", padx=8)

        row = tk.Frame(f); row.pack(fill="x", padx=12, pady=8)
        self.lbl_s_font = tk.Label(row, text=""); self.lbl_s_font.pack(side="left")
        self.spin_font = tk.Spinbox(row, from_=8, to=20, width=4, textvariable=self.var_font)
        self.spin_font.pack(side="left", padx=8)
        self.var_font.trace_add("write", lambda *a: self._on_font_change())

        row = tk.Frame(f); row.pack(fill="x", padx=12, pady=8)
        self.lbl_s_accent = tk.Label(row, text=""); self.lbl_s_accent.pack(side="left")
        self.btn_accent = tk.Button(row, command=self._choose_accent)
        self.btn_accent.pack(side="left", padx=8)

        row = tk.Frame(f); row.pack(fill="x", padx=12, pady=16)
        self.btn_reset = tk.Button(row, command=self._reset_style)
        self.btn_reset.pack(side="left")

    def _build_about_tab(self):
        f = self.tab_about
        self.about_text = tk.Text(f, wrap="word", bd=0, height=20)
        self.about_text.pack(fill="both", expand=True, padx=12, pady=12)

    # ------- estilos -------
    def _paint(self, widget, s, base_font, title_font):
        bg = s["bg"]; fg = s["fg"]
        accent = self.custom_accent or s["accent"]
        accent_fg = s["accent_fg"]
        btn_bg = s["button_bg"]
        entry_bg = s["entry_bg"]; entry_fg = s["entry_fg"]

        for child in widget.winfo_children():
            try:
                if isinstance(child, tk.Frame):
                    child.configure(bg=bg)
                elif isinstance(child, tk.Label):
                    if child is self.lbl_title:
                        child.configure(bg=bg, fg=accent, font=title_font)
                    elif child is self.lbl_version:
                        child.configure(bg=bg, fg=fg, font=base_font)
                    else:
                        child.configure(bg=bg, fg=fg, font=base_font)
                elif isinstance(child, tk.Entry):
                    child.configure(bg=entry_bg, fg=entry_fg, insertbackground=fg,
                                    font=base_font, relief="flat", bd=0,
                                    highlightthickness=1,
                                    highlightbackground=btn_bg, highlightcolor=accent)
                elif isinstance(child, tk.Button):
                    child.configure(bg=btn_bg, fg=fg,
                                    activebackground=accent, activeforeground=accent_fg,
                                    font=base_font,
                                    relief=s.get("button_relief", "flat"),
                                    bd=s.get("button_bd", 0),
                                    padx=10, pady=4)
                elif isinstance(child, tk.Spinbox):
                    child.configure(bg=entry_bg, fg=entry_fg,
                                    buttonbackground=btn_bg,
                                    font=base_font, relief="flat", bd=0)
                elif isinstance(child, tk.Text):
                    child.configure(bg=entry_bg, fg=entry_fg, insertbackground=fg,
                                    font=base_font, relief="flat", bd=0)
                elif isinstance(child, tk.Menubutton):
                    child.configure(bg=btn_bg, fg=fg,
                                    activebackground=accent, activeforeground=accent_fg,
                                    font=base_font, relief="flat", bd=0)
            except Exception:
                pass
            self._paint(child, s, base_font, title_font)

    def apply_style(self):
        s = STYLES[self.style_name]
        bg = s["bg"]; fg = s["fg"]
        accent = self.custom_accent or s["accent"]
        accent_fg = s["accent_fg"]

        base_font = ("Segoe UI", self.font_size)
        title_font = ("Segoe UI", self.font_size + 6, "bold")

        try:
            self.configure(bg=bg)
        except Exception:
            pass

        if hasattr(self, "header"):
            try: self.header.configure(bg=bg)
            except Exception: pass
        if hasattr(self, "lbl_title"):
            try: self.lbl_title.configure(bg=bg, fg=accent, font=title_font)
            except Exception: pass
        if hasattr(self, "lbl_version"):
            try: self.lbl_version.configure(bg=bg, fg=fg, font=base_font)
            except Exception: pass

        # ttk Notebook
        try:
            self.style = ttk.Style(self)
            try:
                self.style.theme_use("clam")
            except Exception:
                pass
            self.style.configure("TNotebook", background=bg, borderwidth=0)
            self.style.configure("TNotebook.Tab", background=s["button_bg"], foreground=fg,
                                 padding=[12, 6], font=base_font)
            self.style.map("TNotebook.Tab",
                           background=[("selected", accent)],
                           foreground=[("selected", accent_fg)])
        except Exception:
            pass

        # pintar árbol
        self._paint(self, s, base_font, title_font)

        # About
        if hasattr(self, "about_text"):
            try:
                self.about_text.configure(bg=s["entry_bg"], fg=s["entry_fg"],
                                          insertbackground=s["fg"],
                                          font=(base_font[0], self.font_size + 1),
                                          relief="flat", bd=0)
            except Exception:
                pass

        # Status bar
        if hasattr(self, "status"):
            try:
                self.status.configure(bg=bg, fg=fg, font=base_font)
            except Exception:
                pass

    # ------- retranslate -------
    def retranslate(self):
        t = self.t
        self.notebook.tab(0, text=t("compress_tab"))
        self.notebook.tab(1, text=t("convert_tab"))
        self.notebook.tab(2, text=t("czip_tab"))
        self.notebook.tab(3, text=t("settings_tab"))
        self.notebook.tab(4, text=t("about_tab"))

        # Compress
        self.lbl_c_in.configure(text=t("input"))
        self.lbl_c_out.configure(text=t("output"))
        self.lbl_c_level.configure(text=t("level"))
        self.btn_c_in.configure(text=t("browse"))
        self.btn_c_out.configure(text=t("browse"))
        self.btn_compress.configure(text=t("compress_btn"))
        self.btn_extract_zip.configure(text=t("extract_btn"))

        # Convert
        self.lbl_v_in.configure(text=t("input"))
        self.lbl_v_detected.configure(text=t("detected") + ":")
        self.lbl_v_target.configure(text=t("target_format"))
        self.lbl_v_out.configure(text=t("output"))
        self.btn_v_in.configure(text=t("browse"))
        self.btn_v_out.configure(text=t("browse"))
        self.btn_convert.configure(text=t("convert_btn"))

        # CZIP
        self.lbl_z_in.configure(text=t("input"))
        self.lbl_z_out.configure(text=t("output"))
        self.lbl_z_pwd.configure(text=t("password"))
        self.btn_z_in.configure(text=t("browse"))
        self.btn_z_out.configure(text=t("browse"))
        self.btn_czip_compress.configure(text=t("czip_compress"))
        self.btn_czip_extract.configure(text=t("czip_extract"))

        # Settings
        self.lbl_s_lang.configure(text=t("language"))
        self.lbl_s_style.configure(text=t("style"))
        self.lbl_s_font.configure(text=t("font_size"))
        self.lbl_s_accent.configure(text=t("accent"))
        self.btn_accent.configure(text=t("choose_color"))
        self.btn_reset.configure(text=t("reset"))

        # About
        self._update_about()

        # Menú
        self._build_menu()

    def _update_about(self):
        if not hasattr(self, "about_text"):
            return
        self.about_text.configure(state="normal")
        self.about_text.delete("1.0", "end")
        self.about_text.insert("1.0", self.t("about_body", lang=self.language))
        self.about_text.configure(state="disabled")

    # ------- callbacks UI -------
    def _on_language_change(self, value):
        self.language = value
        self.retranslate()
        self.apply_style()

    def _on_style_change(self, value):
        self.style_name = value
        self.custom_accent = None
        self.apply_style()

    def _on_font_change(self, *a):
        try:
            size = int(self.var_font.get())
            if 8 <= size <= 20:
                self.font_size = size
                self.apply_style()
        except Exception:
            pass

    def _choose_accent(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.custom_accent = color
            self.apply_style()

    def _reset_style(self):
        self.custom_accent = None
        self.style_name = "Comprimed-ZIP"
        self.var_style.set(self.style_name)
        self.font_size = 10
        self.var_font.set("10")
        self.apply_style()

    # ------- pickers -------
    def pick_compress_in(self):
        p = filedialog.askopenfilename()
        if p:
            self.var_compress_in.set(p)
            base = os.path.splitext(p)[0]
            self.var_compress_out.set(base + ".zip")

    def pick_compress_out(self):
        p = filedialog.asksaveasfilename(defaultextension=".zip",
                                         filetypes=[("ZIP", "*.zip"), ("Todos", "*.*")])
        if p:
            self.var_compress_out.set(p)

    def pick_convert_in(self):
        p = filedialog.askopenfilename()
        if p:
            self.var_convert_in.set(p)
            self._refresh_convert_formats()

    def pick_convert_out(self):
        p = filedialog.asksaveasfilename()
        if p:
            self.var_convert_out.set(p)

    def pick_czip_in(self):
        p = filedialog.askopenfilename(filetypes=[("Comprimed-ZIP", "*.czip"), ("Todos", "*.*")])
        if not p:
            p = filedialog.askopenfilename()
        if p:
            self.var_czip_in.set(p)
            self.var_czip_out.set(os.path.splitext(p)[0] + ".czip")

    def pick_czip_out(self):
        p = filedialog.asksaveasfilename(defaultextension=".czip",
                                         filetypes=[("Comprimed-ZIP", "*.czip")])
        if p:
            self.var_czip_out.set(p)

    def _refresh_convert_formats(self):
        src = self.var_convert_in.get().strip()
        ext = os.path.splitext(src)[1].lower() if src else ""
        self.var_convert_detected.set(ext or "-")
        targets = CONVERSIONS.get(ext, [])
        menu = self.opt_convert_target["menu"]
        menu.delete(0, "end")
        if targets:
            for tgt in targets:
                menu.add_command(label=tgt,
                                 command=lambda t=tgt: self.var_convert_target.set(t))
            self.var_convert_target.set(targets[0])
        else:
            self.var_convert_target.set("")

    # ------- acciones -------
    def do_compress(self):
        src = self.var_compress_in.get().strip()
        if not src or not os.path.isfile(src):
            messagebox.showerror(self.t("error"), self.t("select_file"))
            return
        dst = self.var_compress_out.get().strip()
        if not dst:
            dst = os.path.splitext(src)[0] + ".zip"
            self.var_compress_out.set(dst)
        level = int(self.var_compress_level.get())
        try:
            with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED,
                                 compresslevel=level) as zf:
                zf.write(src, arcname=os.path.basename(src))
            orig = os.path.getsize(src)
            final = os.path.getsize(dst)
            self.set_status("done")
            messagebox.showinfo(self.t("success"),
                                self.t("compressed_msg", orig=orig, final=final))
        except Exception as e:
            messagebox.showerror(self.t("error"), str(e))

    def do_extract_zip(self):
        src = self.var_compress_in.get().strip()
        if not src or not os.path.isfile(src) or not zipfile.is_zipfile(src):
            messagebox.showerror(self.t("error"), self.t("select_file"))
            return
        out_dir = filedialog.askdirectory()
        if not out_dir:
            return
        try:
            with zipfile.ZipFile(src) as zf:
                zf.extractall(out_dir)
            self.set_status("done")
            messagebox.showinfo(self.t("success"), self.t("extracted_msg"))
        except Exception as e:
            messagebox.showerror(self.t("error"), str(e))

    def do_convert(self):
        src = self.var_convert_in.get().strip()
        target = self.var_convert_target.get().strip()
        if not src or not os.path.isfile(src):
            messagebox.showerror(self.t("error"), self.t("select_file"))
            return
        if not target:
            messagebox.showerror(self.t("error"), self.t("target_format"))
            return
        dst = self.var_convert_out.get().strip()
        if not dst:
            dst = os.path.splitext(src)[0] + target
            self.var_convert_out.set(dst)
        try:
            convert_file(src, target, dst)
            self.set_status("done")
            messagebox.showinfo(self.t("success"), self.t("converted_msg"))
        except Exception as e:
            messagebox.showerror(self.t("error"), str(e))

    def do_czip_compress(self):
        src = self.var_czip_in.get().strip()
        if not src or not os.path.isfile(src):
            messagebox.showerror(self.t("error"), self.t("select_file"))
            return
        pwd = self.var_czip_pwd.get()
        if not pwd:
            pwd = simpledialog.askstring(self.t("password"),
                                         self.t("enter_password"), show="*", parent=self)
            if not pwd:
                return
        dst = self.var_czip_out.get().strip() or os.path.splitext(src)[0] + ".czip"
        try:
            write_czip(src, dst, pwd, 9)
            self.var_czip_out.set(dst)
            self.set_status("done")
            messagebox.showinfo(self.t("success"),
                                self.t("compressed_msg",
                                       orig=os.path.getsize(src),
                                       final=os.path.getsize(dst)))
        except Exception as e:
            messagebox.showerror(self.t("error"), str(e))

    def do_czip_extract(self):
        src = self.var_czip_in.get().strip()
        if not src or not os.path.isfile(src) or not src.lower().endswith(".czip"):
            messagebox.showerror(self.t("error"), self.t("select_czip"))
            return
        pwd = self.var_czip_pwd.get()
        if not pwd:
            pwd = simpledialog.askstring(self.t("password"),
                                         self.t("enter_password"), show="*", parent=self)
            if not pwd:
                return
        dst = filedialog.asksaveasfilename()
        if not dst:
            return
        try:
            read_czip(src, dst, pwd)
            self.set_status("done")
            messagebox.showinfo(self.t("success"), self.t("extracted_msg"))
        except Exception:
            messagebox.showerror(self.t("error"), self.t("wrong_password"))

    # ------- HTML -------
    def export_html(self):
        path = filedialog.asksaveasfilename(defaultextension=".html",
                                            initialfile="comprimed_zip.html",
                                            filetypes=[("HTML", "*.html")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(generate_html(self.language, self.style_name))
            messagebox.showinfo(self.t("success"), path)
        except Exception as e:
            messagebox.showerror(self.t("error"), str(e))


# ---------------------------------------------------------------------------
# HTML export
# ---------------------------------------------------------------------------
def generate_html(lang: str, style: str) -> str:
    tr = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
    about = tr["about_body"].format(lang=lang)
    about_html = about.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Comprimed-ZIP 1.0</title>
<style>
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; background:#1e1e2e; color:#cdd6f4; margin:0; padding:24px; }}
  h1 {{ color:#89b4fa; margin:0 0 8px 0; }}
  .card {{ background:#313244; border-radius:12px; padding:24px; max-width:720px; margin:0 auto; }}
  pre {{ background:#181825; padding:16px; border-radius:8px; overflow:auto; }}
  small {{ color:#9399b2; }}
</style>
</head>
<body>
<div class="card">
  <h1>Comprimed-ZIP <small>v1.0</small></h1>
  <p>Estilo exportado: <b>{style}</b> · Idioma: <b>{lang}</b></p>
  <h2>Acerca de</h2>
  <pre>{about_html}</pre>
  <p><small>David© - Comprimed-ZIP 2026</small></p>
</div>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = ComprimedZIP()
    app.mainloop()
