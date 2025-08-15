"""
نظام الترجمة للبوت
يحتوي على جميع النصوص المطلوبة بعدة لغات
"""

class BotTranslations:
    def __init__(self):
        self.translations = {
            'ar': {
                # رسائل الترحيب والقوائم الرئيسية
                'welcome_authenticated': "🎉 أهلاً بك في بوت التوجيه التلقائي!\n\n👋 مرحباً {name}\n🔑 حالة تسجيل الدخول: نشطة\n🤖 UserBot: {status}\n\n💡 النظام الجديد:\n• بوت التحكم منفصل عن UserBot\n• يمكنك إدارة المهام دائماً\n• إذا تعطل UserBot، أعد تسجيل الدخول\n\nاختر ما تريد فعله:",
                'welcome_unauthenticated': "🤖 مرحباً بك في بوت التوجيه التلقائي!\n\n📋 هذا البوت يساعدك في:\n• توجيه الرسائل تلقائياً\n• إدارة مهام التوجيه\n• مراقبة المحادثات\n\n🔐 يجب تسجيل الدخول أولاً:",
                'system_status_active': "🟢 نشط",
                'system_status_inactive': "🟡 مطلوب فحص",
                
                # أزرار القوائم
                'btn_manage_tasks': "📝 إدارة مهام التوجيه",
                'btn_check_userbot': "🔍 فحص حالة UserBot",
                'btn_settings': "⚙️ الإعدادات",
                'btn_about': "ℹ️ حول البوت",
                'btn_login_phone': "📱 تسجيل الدخول برقم الهاتف",
                'btn_back_to_main': "🏠 القائمة الرئيسية",
                'btn_back_to_settings': "🔙 العودة للإعدادات",
                
                # إعدادات اللغة والمنطقة الزمنية
                'language_settings_title': "🌐 **اختر اللغة المفضلة:**",
                'timezone_settings_title': "🕐 **اختر المنطقة الزمنية:**",
                'settings_title': "⚙️ **إعدادات البوت**\n\n🌐 اللغة الحالية: {language}\n🕐 المنطقة الزمنية الحالية: {timezone}\n\nاختر الإعداد الذي تريد تغييره:",
                
                # رسائل النجاح والخطأ
                'language_changed_success': "✅ تم تغيير اللغة إلى {language}",
                'language_change_failed': "❌ فشل في تغيير اللغة",
                'timezone_changed_success': "✅ تم تغيير المنطقة الزمنية إلى {timezone}",
                'timezone_change_failed': "❌ فشل في تغيير المنطقة الزمنية",
                
                # أسماء اللغات
                'lang_arabic': "🇸🇦 العربية",
                'lang_english': "🇺🇸 English",
                'lang_french': "🇫🇷 Français",
                'lang_german': "🇩🇪 Deutsch",
                'lang_spanish': "🇪🇸 Español",
                'lang_russian': "🇷🇺 Русский",
                
                # إدارة المهام
                'tasks_menu_title': "📝 **إدارة مهام التوجيه**\n\nاختر العملية التي تريد تنفيذها:",
                'btn_create_task': "➕ إنشاء مهمة جديدة",
                'btn_list_tasks': "📋 عرض المهام الحالية",
                'btn_task_statistics': "📊 إحصائيات المهام",
                
                # حالة المهام
                'task_active': "🟢 نشطة",
                'task_inactive': "🔴 غير نشطة",
                'task_paused': "🟡 متوقفة مؤقتاً",
                
                # الفلاتر
                'advanced_filters_title': "🔍 الفلاتر المتقدمة - المهمة #{task_id}",
                'language_filter': "فلتر اللغات",
                'day_filter': "فلتر الأيام",
                'time_filter': "ساعات العمل",
                'admin_filter': "فلتر المشرفين",
                'duplicate_filter': "فلتر التكرار",
                'forwarded_filter': "الرسائل المُوجهة",
                
                # رسائل عامة
                'error_occurred': "❌ حدث خطأ غير متوقع",
                'operation_cancelled': "🚫 تم إلغاء العملية",
                'please_wait': "⏳ يرجى الانتظار...",
                'processing': "🔄 جاري المعالجة...",
                'completed': "✅ تم بنجاح",
                'failed': "❌ فشل في العملية",
                
                # نصوص إضافية
                'btn_change_language': "🌐 تغيير اللغة",
                'btn_change_timezone': "🕐 تغيير المنطقة الزمنية",
                'btn_delete_all_tasks': "🗑️ حذف جميع المهام",
                'btn_relogin': "🔄 إعادة تسجيل الدخول",
                'total_tasks': "إجمالي المهام",
                'active_tasks': "المهام النشطة",
                'inactive_tasks': "المهام المتوقفة",
                'statistics': "الإحصائيات",
                'choose_action': "اختر إجراء",
            },
            
            'en': {
                # Welcome messages and main menus
                'welcome_authenticated': "🎉 Welcome to the Auto-Forwarding Bot!\n\n👋 Hello {name}\n🔑 Login status: Active\n🤖 UserBot: {status}\n\n💡 New system:\n• Control bot is separate from UserBot\n• You can always manage tasks\n• If UserBot fails, re-login\n\nChoose what you want to do:",
                'welcome_unauthenticated': "🤖 Welcome to the Auto-Forwarding Bot!\n\n📋 This bot helps you with:\n• Automatic message forwarding\n• Managing forwarding tasks\n• Monitoring conversations\n\n🔐 You need to login first:",
                'system_status_active': "🟢 Active",
                'system_status_inactive': "🟡 Check required",
                
                # Menu buttons
                'btn_manage_tasks': "📝 Manage Forwarding Tasks",
                'btn_check_userbot': "🔍 Check UserBot Status",
                'btn_settings': "⚙️ Settings",
                'btn_about': "ℹ️ About Bot",
                'btn_login_phone': "📱 Login with Phone Number",
                'btn_back_to_main': "🏠 Main Menu",
                'btn_back_to_settings': "🔙 Back to Settings",
                
                # Language and timezone settings
                'language_settings_title': "🌐 **Choose your preferred language:**",
                'timezone_settings_title': "🕐 **Choose your timezone:**",
                'settings_title': "⚙️ **Bot Settings**\n\n🌐 Current language: {language}\n🕐 Current timezone: {timezone}\n\nChoose the setting you want to change:",
                
                # Success and error messages
                'language_changed_success': "✅ Language changed to {language}",
                'language_change_failed': "❌ Failed to change language",
                'timezone_changed_success': "✅ Timezone changed to {timezone}",
                'timezone_change_failed': "❌ Failed to change timezone",
                
                # Language names
                'lang_arabic': "🇸🇦 العربية",
                'lang_english': "🇺🇸 English",
                'lang_french': "🇫🇷 Français",
                'lang_german': "🇩🇪 Deutsch",
                'lang_spanish': "🇪🇸 Español",
                'lang_russian': "🇷🇺 Русский",
                
                # Task management
                'tasks_menu_title': "📝 **Manage Forwarding Tasks**\n\nChoose the operation you want to perform:",
                'btn_create_task': "➕ Create New Task",
                'btn_list_tasks': "📋 View Current Tasks",
                'btn_task_statistics': "📊 Task Statistics",
                
                # Task status
                'task_active': "🟢 Active",
                'task_inactive': "🔴 Inactive",
                'task_paused': "🟡 Paused",
                
                # Filters
                'advanced_filters_title': "🔍 Advanced Filters - Task #{task_id}",
                'language_filter': "Language Filter",
                'day_filter': "Day Filter",
                'time_filter': "Working Hours",
                'admin_filter': "Admin Filter",
                'duplicate_filter': "Duplicate Filter",
                'forwarded_filter': "Forwarded Messages",
                
                # General messages
                'error_occurred': "❌ An unexpected error occurred",
                'operation_cancelled': "🚫 Operation cancelled",
                'please_wait': "⏳ Please wait...",
                'processing': "🔄 Processing...",
                'completed': "✅ Completed successfully",
                'failed': "❌ Operation failed",
                
                # Additional texts
                'btn_change_language': "🌐 Change Language",
                'btn_change_timezone': "🕐 Change Timezone",
                'btn_delete_all_tasks': "🗑️ Delete All Tasks",
                'btn_relogin': "🔄 Re-login",
                'total_tasks': "Total Tasks",
                'active_tasks': "Active Tasks",
                'inactive_tasks': "Inactive Tasks",
                'statistics': "Statistics",
                'choose_action': "Choose Action",
            },
            
            'fr': {
                # Messages de bienvenue et menus principaux
                'welcome_authenticated': "🎉 Bienvenue dans le Bot de Transfert Automatique!\n\n👋 Bonjour {name}\n🔑 Statut de connexion: Actif\n🤖 UserBot: {status}\n\n💡 Nouveau système:\n• Le bot de contrôle est séparé d'UserBot\n• Vous pouvez toujours gérer les tâches\n• Si UserBot échoue, reconnectez-vous\n\nChoisissez ce que vous voulez faire:",
                'welcome_unauthenticated': "🤖 Bienvenue dans le Bot de Transfert Automatique!\n\n📋 Ce bot vous aide avec:\n• Transfert automatique de messages\n• Gestion des tâches de transfert\n• Surveillance des conversations\n\n🔐 Vous devez d'abord vous connecter:",
                'system_status_active': "🟢 Actif",
                'system_status_inactive': "🟡 Vérification requise",
                
                # Boutons de menu
                'btn_manage_tasks': "📝 Gérer les Tâches de Transfert",
                'btn_check_userbot': "🔍 Vérifier le Statut UserBot",
                'btn_settings': "⚙️ Paramètres",
                'btn_about': "ℹ️ À propos du Bot",
                'btn_login_phone': "📱 Connexion avec Numéro de Téléphone",
                'btn_back_to_main': "🏠 Menu Principal",
                'btn_back_to_settings': "🔙 Retour aux Paramètres",
                
                # Paramètres de langue et fuseau horaire
                'language_settings_title': "🌐 **Choisissez votre langue préférée:**",
                'timezone_settings_title': "🕐 **Choisissez votre fuseau horaire:**",
                'settings_title': "⚙️ **Paramètres du Bot**\n\n🌐 Langue actuelle: {language}\n🕐 Fuseau horaire actuel: {timezone}\n\nChoisissez le paramètre que vous voulez modifier:",
                
                # Messages de succès et d'erreur
                'language_changed_success': "✅ Langue changée en {language}",
                'language_change_failed': "❌ Échec du changement de langue",
                'timezone_changed_success': "✅ Fuseau horaire changé en {timezone}",
                'timezone_change_failed': "❌ Échec du changement de fuseau horaire",
                
                # Noms des langues
                'lang_arabic': "🇸🇦 العربية",
                'lang_english': "🇺🇸 English",
                'lang_french': "🇫🇷 Français",
                'lang_german': "🇩🇪 Deutsch",
                'lang_spanish': "🇪🇸 Español",
                'lang_russian': "🇷🇺 Русский",
                
                # Gestion des tâches
                'tasks_menu_title': "📝 **Gérer les Tâches de Transfert**\n\nChoisissez l'opération que vous voulez effectuer:",
                'btn_create_task': "➕ Créer une Nouvelle Tâche",
                'btn_list_tasks': "📋 Voir les Tâches Actuelles",
                'btn_task_statistics': "📊 Statistiques des Tâches",
                
                # Statut des tâches
                'task_active': "🟢 Actif",
                'task_inactive': "🔴 Inactif",
                'task_paused': "🟡 En pause",
                
                # Filtres
                'advanced_filters_title': "🔍 Filtres Avancés - Tâche #{task_id}",
                'language_filter': "Filtre de Langue",
                'day_filter': "Filtre de Jour",
                'time_filter': "Heures de Travail",
                'admin_filter': "Filtre Administrateur",
                'duplicate_filter': "Filtre de Doublons",
                'forwarded_filter': "Messages Transférés",
                
                # Messages généraux
                'error_occurred': "❌ Une erreur inattendue s'est produite",
                'operation_cancelled': "🚫 Opération annulée",
                'please_wait': "⏳ Veuillez patienter...",
                'processing': "🔄 Traitement en cours...",
                'completed': "✅ Terminé avec succès",
                'failed': "❌ Opération échouée",
                
                # Textes supplémentaires
                'btn_change_language': "🌐 Changer la Langue",
                'btn_change_timezone': "🕐 Changer le Fuseau Horaire",
                'btn_delete_all_tasks': "🗑️ Supprimer Toutes les Tâches",
                'btn_relogin': "🔄 Se Reconnecter",
                'total_tasks': "Total des Tâches",
                'active_tasks': "Tâches Actives",
                'inactive_tasks': "Tâches Inactives",
                'statistics': "Statistiques",
                'choose_action': "Choisir une Action",
            },
            
            'de': {
                # Willkommensnachrichten und Hauptmenüs
                'welcome_authenticated': "🎉 Willkommen beim Auto-Weiterleitungs-Bot!\n\n👋 Hallo {name}\n🔑 Anmeldestatus: Aktiv\n🤖 UserBot: {status}\n\n💡 Neues System:\n• Kontroll-Bot ist getrennt von UserBot\n• Sie können Aufgaben immer verwalten\n• Falls UserBot fehlschlägt, melden Sie sich neu an\n\nWählen Sie, was Sie tun möchten:",
                'welcome_unauthenticated': "🤖 Willkommen beim Auto-Weiterleitungs-Bot!\n\n📋 Dieser Bot hilft Ihnen bei:\n• Automatische Nachrichtenweiterleitung\n• Verwaltung von Weiterleitungsaufgaben\n• Überwachung von Gesprächen\n\n🔐 Sie müssen sich zuerst anmelden:",
                'system_status_active': "🟢 Aktiv",
                'system_status_inactive': "🟡 Überprüfung erforderlich",
                
                # Menü-Buttons
                'btn_manage_tasks': "📝 Weiterleitungsaufgaben Verwalten",
                'btn_check_userbot': "🔍 UserBot-Status Prüfen",
                'btn_settings': "⚙️ Einstellungen",
                'btn_about': "ℹ️ Über Bot",
                'btn_login_phone': "📱 Mit Telefonnummer Anmelden",
                'btn_back_to_main': "🏠 Hauptmenü",
                'btn_back_to_settings': "🔙 Zurück zu Einstellungen",
                
                # Sprach- und Zeitzoneneinstellungen
                'language_settings_title': "🌐 **Wählen Sie Ihre bevorzugte Sprache:**",
                'timezone_settings_title': "🕐 **Wählen Sie Ihre Zeitzone:**",
                'settings_title': "⚙️ **Bot-Einstellungen**\n\n🌐 Aktuelle Sprache: {language}\n🕐 Aktuelle Zeitzone: {timezone}\n\nWählen Sie die Einstellung, die Sie ändern möchten:",
                
                # Erfolgs- und Fehlermeldungen
                'language_changed_success': "✅ Sprache geändert zu {language}",
                'language_change_failed': "❌ Sprache konnte nicht geändert werden",
                'timezone_changed_success': "✅ Zeitzone geändert zu {timezone}",
                'timezone_change_failed': "❌ Zeitzone konnte nicht geändert werden",
                
                # Sprachnamen
                'lang_arabic': "🇸🇦 العربية",
                'lang_english': "🇺🇸 English",
                'lang_french': "🇫🇷 Français",
                'lang_german': "🇩🇪 Deutsch",
                'lang_spanish': "🇪🇸 Español",
                'lang_russian': "🇷🇺 Русский",
                
                # Aufgabenverwaltung
                'tasks_menu_title': "📝 **Weiterleitungsaufgaben Verwalten**\n\nWählen Sie die Aktion, die Sie ausführen möchten:",
                'btn_create_task': "➕ Neue Aufgabe Erstellen",
                'btn_list_tasks': "📋 Aktuelle Aufgaben Anzeigen",
                'btn_task_statistics': "📊 Aufgabenstatistiken",
                
                # Aufgabenstatus
                'task_active': "🟢 Aktiv",
                'task_inactive': "🔴 Inaktiv",
                'task_paused': "🟡 Pausiert",
                
                # Filter
                'advanced_filters_title': "🔍 Erweiterte Filter - Aufgabe #{task_id}",
                'language_filter': "Sprachfilter",
                'day_filter': "Tagesfilter",
                'time_filter': "Arbeitszeiten",
                'admin_filter': "Admin-Filter",
                'duplicate_filter': "Duplikat-Filter",
                'forwarded_filter': "Weitergeleitete Nachrichten",
                
                # Allgemeine Nachrichten
                'error_occurred': "❌ Ein unerwarteter Fehler ist aufgetreten",
                'operation_cancelled': "🚫 Vorgang abgebrochen",
                'please_wait': "⏳ Bitte warten...",
                'processing': "🔄 Verarbeitung läuft...",
                'completed': "✅ Erfolgreich abgeschlossen",
                'failed': "❌ Vorgang fehlgeschlagen",
                
                # Zusätzliche Texte
                'btn_change_language': "🌐 Sprache Ändern",
                'btn_change_timezone': "🕐 Zeitzone Ändern",
                'btn_delete_all_tasks': "🗑️ Alle Aufgaben Löschen",
                'btn_relogin': "🔄 Neu Anmelden",
                'total_tasks': "Gesamte Aufgaben",
                'active_tasks': "Aktive Aufgaben",
                'inactive_tasks': "Inaktive Aufgaben",
                'statistics': "Statistiken",
                'choose_action': "Aktion Wählen",
            },
            
            'es': {
                # Mensajes de bienvenida y menús principales
                'welcome_authenticated': "🎉 ¡Bienvenido al Bot de Reenvío Automático!\n\n👋 Hola {name}\n🔑 Estado de inicio de sesión: Activo\n🤖 UserBot: {status}\n\n💡 Nuevo sistema:\n• Bot de control separado de UserBot\n• Siempre puedes gestionar tareas\n• Si UserBot falla, vuelve a iniciar sesión\n\nElige qué quieres hacer:",
                'welcome_unauthenticated': "🤖 ¡Bienvenido al Bot de Reenvío Automático!\n\n📋 Este bot te ayuda con:\n• Reenvío automático de mensajes\n• Gestión de tareas de reenvío\n• Monitoreo de conversaciones\n\n🔐 Primero necesitas iniciar sesión:",
                'system_status_active': "🟢 Activo",
                'system_status_inactive': "🟡 Verificación requerida",
                
                # Botones de menú
                'btn_manage_tasks': "📝 Gestionar Tareas de Reenvío",
                'btn_check_userbot': "🔍 Verificar Estado de UserBot",
                'btn_settings': "⚙️ Configuración",
                'btn_about': "ℹ️ Acerca del Bot",
                'btn_login_phone': "📱 Iniciar Sesión con Número de Teléfono",
                'btn_back_to_main': "🏠 Menú Principal",
                'btn_back_to_settings': "🔙 Volver a Configuración",
                
                # Configuración de idioma y zona horaria
                'language_settings_title': "🌐 **Elige tu idioma preferido:**",
                'timezone_settings_title': "🕐 **Elige tu zona horaria:**",
                'settings_title': "⚙️ **Configuración del Bot**\n\n🌐 Idioma actual: {language}\n🕐 Zona horaria actual: {timezone}\n\nElige la configuración que quieres cambiar:",
                
                # Mensajes de éxito y error
                'language_changed_success': "✅ Idioma cambiado a {language}",
                'language_change_failed': "❌ Falló el cambio de idioma",
                'timezone_changed_success': "✅ Zona horaria cambiada a {timezone}",
                'timezone_change_failed': "❌ Falló el cambio de zona horaria",
                
                # Nombres de idiomas
                'lang_arabic': "🇸🇦 العربية",
                'lang_english': "🇺🇸 English",
                'lang_french': "🇫🇷 Français",
                'lang_german': "🇩🇪 Deutsch",
                'lang_spanish': "🇪🇸 Español",
                'lang_russian': "🇷🇺 Русский",
                
                # Gestión de tareas
                'tasks_menu_title': "📝 **Gestionar Tareas de Reenvío**\n\nElige la operación que quieres realizar:",
                'btn_create_task': "➕ Crear Nueva Tarea",
                'btn_list_tasks': "📋 Ver Tareas Actuales",
                'btn_task_statistics': "📊 Estadísticas de Tareas",
                
                # Estado de tareas
                'task_active': "🟢 Activo",
                'task_inactive': "🔴 Inactivo",
                'task_paused': "🟡 Pausado",
                
                # Filtros
                'advanced_filters_title': "🔍 Filtros Avanzados - Tarea #{task_id}",
                'language_filter': "Filtro de Idioma",
                'day_filter': "Filtro de Día",
                'time_filter': "Horario de Trabajo",
                'admin_filter': "Filtro de Administrador",
                'duplicate_filter': "Filtro de Duplicados",
                'forwarded_filter': "Mensajes Reenviados",
                
                # Mensajes generales
                'error_occurred': "❌ Ocurrió un error inesperado",
                'operation_cancelled': "🚫 Operación cancelada",
                'please_wait': "⏳ Por favor espera...",
                'processing': "🔄 Procesando...",
                'completed': "✅ Completado exitosamente",
                'failed': "❌ Operación fallida",
                
                # Textos adicionales
                'btn_change_language': "🌐 Cambiar Idioma",
                'btn_change_timezone': "🕐 Cambiar Zona Horaria",
                'btn_delete_all_tasks': "🗑️ Eliminar Todas las Tareas",
                'btn_relogin': "🔄 Volver a Iniciar Sesión",
                'total_tasks': "Total de Tareas",
                'active_tasks': "Tareas Activas",
                'inactive_tasks': "Tareas Inactivas",
                'statistics': "Estadísticas",
                'choose_action': "Elegir Acción",
            },
            
            'ru': {
                # Приветственные сообщения и главные меню
                'welcome_authenticated': "🎉 Добро пожаловать в Бот Автопересылки!\n\n👋 Привет {name}\n🔑 Статус входа: Активен\n🤖 UserBot: {status}\n\n💡 Новая система:\n• Управляющий бот отделён от UserBot\n• Вы всегда можете управлять задачами\n• Если UserBot не работает, войдите заново\n\nВыберите, что хотите сделать:",
                'welcome_unauthenticated': "🤖 Добро пожаловать в Бот Автопересылки!\n\n📋 Этот бот поможет вам с:\n• Автоматической пересылкой сообщений\n• Управлением задачами пересылки\n• Мониторингом разговоров\n\n🔐 Сначала нужно войти в систему:",
                'system_status_active': "🟢 Активен",
                'system_status_inactive': "🟡 Требуется проверка",
                
                # Кнопки меню
                'btn_manage_tasks': "📝 Управление Задачами Пересылки",
                'btn_check_userbot': "🔍 Проверить Статус UserBot",
                'btn_settings': "⚙️ Настройки",
                'btn_about': "ℹ️ О Боте",
                'btn_login_phone': "📱 Войти по Номеру Телефона",
                'btn_back_to_main': "🏠 Главное Меню",
                'btn_back_to_settings': "🔙 Назад к Настройкам",
                
                # Настройки языка и часового пояса
                'language_settings_title': "🌐 **Выберите предпочитаемый язык:**",
                'timezone_settings_title': "🕐 **Выберите ваш часовой пояс:**",
                'settings_title': "⚙️ **Настройки Бота**\n\n🌐 Текущий язык: {language}\n🕐 Текущий часовой пояс: {timezone}\n\nВыберите настройку, которую хотите изменить:",
                
                # Сообщения успеха и ошибки
                'language_changed_success': "✅ Язык изменён на {language}",
                'language_change_failed': "❌ Не удалось изменить язык",
                'timezone_changed_success': "✅ Часовой пояс изменён на {timezone}",
                'timezone_change_failed': "❌ Не удалось изменить часовой пояс",
                
                # Названия языков
                'lang_arabic': "🇸🇦 العربية",
                'lang_english': "🇺🇸 English",
                'lang_french': "🇫🇷 Français",
                'lang_german': "🇩🇪 Deutsch",
                'lang_spanish': "🇪🇸 Español",
                'lang_russian': "🇷🇺 Русский",
                
                # Управление задачами
                'tasks_menu_title': "📝 **Управление Задачами Пересылки**\n\nВыберите операцию, которую хотите выполнить:",
                'btn_create_task': "➕ Создать Новую Задачу",
                'btn_list_tasks': "📋 Просмотреть Текущие Задачи",
                'btn_task_statistics': "📊 Статистика Задач",
                
                # Статус задач
                'task_active': "🟢 Активна",
                'task_inactive': "🔴 Неактивна",
                'task_paused': "🟡 Приостановлена",
                
                # Фильтры
                'advanced_filters_title': "🔍 Расширенные Фильтры - Задача #{task_id}",
                'language_filter': "Языковой Фильтр",
                'day_filter': "Фильтр Дней",
                'time_filter': "Рабочие Часы",
                'admin_filter': "Фильтр Администратора",
                'duplicate_filter': "Фильтр Дубликатов",
                'forwarded_filter': "Пересланные Сообщения",
                
                # Общие сообщения
                'error_occurred': "❌ Произошла неожиданная ошибка",
                'operation_cancelled': "🚫 Операция отменена",
                'please_wait': "⏳ Пожалуйста, подождите...",
                'processing': "🔄 Обработка...",
                'completed': "✅ Успешно завершено",
                'failed': "❌ Операция не удалась",
                
                # Дополнительные тексты
                'btn_change_language': "🌐 Изменить Язык",
                'btn_change_timezone': "🕐 Изменить Часовой Пояс",
                'btn_delete_all_tasks': "🗑️ Удалить Все Задачи",
                'btn_relogin': "🔄 Войти Заново",
                'total_tasks': "Всего Задач",
                'active_tasks': "Активные Задачи",
                'inactive_tasks': "Неактивные Задачи",
                'statistics': "Статистика",
                'choose_action': "Выберите Действие",
            }
        }
    
    def get_text(self, key, language='ar', **kwargs):
        """
        الحصول على النص المترجم
        
        Args:
            key: مفتاح النص
            language: رمز اللغة (افتراضي: ar)
            **kwargs: متغيرات لتنسيق النص
        
        Returns:
            النص المترجم أو النص بالعربية إذا لم توجد الترجمة
        """
        # التأكد من أن اللغة مدعومة
        if language not in self.translations:
            language = 'ar'  # العودة للعربية كلغة افتراضية
        
        # الحصول على النص
        text = self.translations[language].get(key, self.translations['ar'].get(key, key))
        
        # تنسيق النص بالمتغيرات المرسلة
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                # في حالة عدم وجود متغير مطلوب، عرض النص كما هو
                pass
        
        return text
    
    def get_language_name(self, language_code):
        """الحصول على اسم اللغة"""
        language_names = {
            'ar': self.get_text('lang_arabic', language_code),
            'en': self.get_text('lang_english', language_code),
            'fr': self.get_text('lang_french', language_code),
            'de': self.get_text('lang_german', language_code),
            'es': self.get_text('lang_spanish', language_code),
            'ru': self.get_text('lang_russian', language_code)
        }
        return language_names.get(language_code, f'{language_code}')
    
    def get_supported_languages(self):
        """الحصول على قائمة اللغات المدعومة"""
        return list(self.translations.keys())

# إنشاء instance عالمي
translations = BotTranslations()