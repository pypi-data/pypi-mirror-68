class Utils:
  def assert_dialog(lambda_function, notification):
    try:
      assert lambda_function()
    except:
      OSA.display_dialog(notification, text_prompt = False, buttons = ["OK"])
  def brewlist(versions=False):
    """
    --versions, you get 1.20.1_4, not necessarily what's in brew search. seems that you tended to use latest version.
    """
    return getoutput("brew list").split("\n")if(versions==False)else(lmap(lambda x: x.replace(" ", "@"), getoutput("brew list --versions").split("\n")))
    """
    brewlist(versions = False)
    brewlist(versions = True)
    """
  def brightness(lvl):
    OSA("System Events", ['brightness %s'%lvl])
  def change_default_file_extension(ext, application_address):
    duti(ext = ext, application_address = application_address)
  def change_mac_address():
    mac_address = subprocess.getoutput("openssl rand -hex 6 | sed 's/\(..\)/\\1:/g; s/.$//'")
    os.system("sudo ifconfig en0 ether %s"%(mac_address))
  def clear_google_chrome_processes():
    tp(lambda:lmap(lambda i: os.system("kill -9 %s" % i), lmap(lambda i: re.sub(r" +"," ",i.strip()).split(" ")[1],subprocess.getoutput("ps -ef | grep Google\ Chrome | grep Profile\ 1000").split("\n"))))
  def duti(ext = "informative", application_address = "/Applications/Sublime Text.app"):
    bundle_identifier = subprocess.getoutput("/usr/libexec/PlistBuddy -c 'Print CFBundleIdentifier' '%s/Contents/Info.plist'" % application_address)
    os.system("brew install duti")if("duti" not in brewlist())else()
    redprint("duti -s %s %s all" % (bundle_identifier, ext))
    os.system("duti -s %s %s all" % (bundle_identifier, ext))
    return
  def generate_keylogger():
    times, keys = [], []
    file = open(userfolder("~/hole/hole/keylogger/logfile.log")).read().split("\n")[:-1]
    file = sudby(lambda i: i.split(" ",1)[1][0] != "[", file)
    for i in file:
      time, key = i.split(" ",1)
      times.append(time)
      keys.append(key)
    time, letters, current_load, on = None, "", "", False
    current_loads = []
    for i, j in zip(times,keys):
      letters = letters + j
      time = i
      if letters.endswith("ss-"):
        on = True
      if on == True:
        current_load = current_load + j
      if letters.endswith("-ee"):
        on = False
        time = i
        current_load = current_load[2:-3]
        print(current_load)
        current_loads.append([time, current_load])
        time = datetime.fromtimestamp(int(time))
        tp(lambda:Save(Note,note=current_load,time=time))
        letters = ""
        current_load = ""
    # if os.path.getsize(userfolder("~/hole/hole/keylogger/logfile.log")) > 7432790:
    #   x = open(userfolder("~/hole/hole/keylogger/logfile.log"),"r").readlines()
    #   num_lines = int(len(x)/2)
    #   y = x[:num_lines]
    #   open(userfolder("~/hole/hole/keylogger/logfile.log"),"w").write("".join(y))
    time.sleep(60)
    ifdo(lambda:random.randrange(1,61) == 60,lambda:os.system("killall keylogger"))
    generate_keylogger()
    # return current_loads
  def get_chmod_statuses():
    for i in os.listdir("/Applications"):
      status = subprocess.getoutput("stat -f '%OLp' '/Applications/{}'".format(i))
      print("%s: %s" % (i,status))
    for i in os.listdir("/Applications/Utilities"):
      status = subprocess.getoutput("stat -f '%OLp' '/Applications/Utilities/{}'".format(i))
      print("%s: %s" % (i,status))
  def getwindowcount(x):
    return int(subprocess.getoutput("""osascript -e 'tell application "%s" to get (count of windows)'"""%x))
  def lid_is_closed():
    lid_is_closed = (False)if("No"in(subprocess.getoutput("ioreg -r -k AppleClamshellState -d 4 | grep AppleClamshellState  | head -1")))else(True)
    return lid_is_closed
  def quicktime_recording():
    os.system("""osascript -e 'tell application "QuickTime Player" to activate' -e 'tell application "QuickTime Player" to start (new screen recording)'""")
  def readministrate():
    import getpass
    os.system("sudo -passwd admin")
    os.system("sudo dscl . -append /Groups/admin GroupMembership %s"%(getpass.getuser()))
  def run_pinterest_board_image_getter():
    # 'https://api.pinterest.com/oauth/?scope=read_public,write_public&client_id=5066656475317842279&state=768uyFys&response_type=code&redirect_uri=https://localhost/auth/pinterest/callback\nhttps://localhost/auth/pinterest/callback?state=768uyFys&code=de928c1c929e5c05\n\n\ndata={"grant_type":"authorization_code",\n"client_id":5066656475317842279,\n"client_secret":"84a1b5a0d3c5fc58fdbf7238902330d042ff2dfcf997c3ee2013c0408b03bb8e",\n"code":"d2021af082c74329",}\nx=requests.post("https://api.pinterest.com/v1/oauth/token",data=data)\n#y=\'{"access_token": "An0Xs7HN42Vf6UlX72a-KVcHjQahFdfH1Ef4bCxGUGE4UkCxZwhtQDAAAsw9RlBjTAqAq3MAAAAA", "token_type": "bearer", "scope": ["read_public", "write_public", "read_private", "write_private", "read_write_all"]}\'\ndata = json.loads(x.text)\naccess_token = data["access_token"]\n\nhttps://api.pinterest.com/v1/boards/396035429671343708/pins/?access_token=An8K8wKh3MUU2SX8uNNQh4I42w_1FcKm1yR6NIlGJA_4Q6Ckiwj7gDAAAqv1RiQTFyGAsh0AAAAA&fields=id%2Clink%2Cnote%2Curl%2Cattribution%2Cboard\n\n\n\nparams = {"access_token":access_token,"fields":["image","note"]}\nr = requests.get("https://api.pinterest.com/v1/boards/whitetiger62/steampunk-girl/pins/",params=params)\nall_data = []\ndata = json.loads(r.text)\nall_data.extend(data["data"])\nwhile "next" in data.get("page",{}):\n  r = requests.get(data["page"]["next"])\n  data = json.loads(r.text)\n  all_data.extend(data["data"])\n  print(data)\n  time.sleep(1)\n\n\nrequests.get("https://api.pinterest.com/v1/me/pins/?access_token=%s&fields=id,note&limit=1"%(access_token))\n\nrequests.get("https://api.pinterest.com/v1/boards/anapinskywalker/wanderlust/pins/?access_token=%s&limit=2&fields=id,link,counts,note"%(access_token))\n'
    process(lambda:OSA.log("x=document.getElementsByTagName('img');y=x.length;l=[];for (i=0;i<y;i++) {l=l.concat(x[i].src);};console.log(l.length);copy(l.join());"))
    datas = []
    while True:
      if pyperclip.paste() not in datas:
        datas.append(pyperclip.paste())
      if pyperclip.paste() == "end":
        break
    datas = listminus(datas,None)
    datas = oset(flatten(lmap(lambda i:i.split(","),sudby(lambda i:i.endswith("jpg"),datas)),1))
    datas = datas[1:]
    datas = lmap(lambda i:re.sub("(https://i.pinimg.com/)\d+x(.*)","\\g<1>1200x\\g<2>",i),datas)
    datas = [i for i in datas if re.findall("https://i.pinimg.com/\d+x\d+_RS",i) == []]
    # file_links = pool(lambda i: Images().download(i),datas,nodes=24)

    return datas
  def screenshot(address=None):
    if address == None:
      os.makedirs(userfolder("~/tavern/tavern/soda/dls"), exist_ok = True)
      address = userfolder("~/tavern/tavern/soda/dls/%s.png"%(random.randrange(9999999999999)))
      magentaprint("generated address: %s" % address)
    greenprint("saving to address: %s" % address)
    os.system("""screencapture -x "{}" """.format(address))
    return address
  def text_to_image(text):
    from PIL import Image, ImageDraw, ImageFont

    if text == "":
      text = "\n"
     
    img = Image.new('RGB', (1800, 540), color = (255, 255, 255))
    fnt = ImageFont.truetype("/Library/Fonts/Times New Roman.ttf", 20)
    d = ImageDraw.Draw(img)
    d.text((0,0), text, font=fnt, fill=(0, 0, 0))
    font_size = d.textsize(text, fnt)

    img = Image.new('RGB', font_size, color = (255, 255, 255))
    fnt = ImageFont.truetype("/Library/Fonts/Times New Roman.ttf", 20)
    d = ImageDraw.Draw(img)
    d.text((0,0), text, font=fnt, fill=(0, 0, 0))

    address = get_random_address(userfolder("~/tavern/tavern/soda/dls")).png()
    img.save(address)
    impreview(address)
    os.remove(address)
  def transfer_workflows():
    [os.system("rm -rf /Users/paul/tavern/tavern/soda/*.workflow"),[os.system("cp -r ~/Library/Services/%s ~/tavern/tavern/soda/%s"%(i,i)) for i in os.listdir(userfolder("~/Library/Services")) if i.endswith(".workflow")]]
  def unadministrate():
    import getpass
    os.system("sudo chmod 000 '/Applications/League of Legends.app'")
    os.system("sudo passwd admin")
    os.system("sudo dseditgroup -o edit -d %s -t user admin"%(getpass.getuser()))
    os.system("dscl . -delete /groups/admin GroupMembership %s"%(getpass.getuser()))
  def xplist(x):
    r = '\n  <?xml version="1.0" encoding="UTF-8"?>\n  <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n  <plist version="1.0">\n  <dict>\n      <key>Label</key>\n      <string>{}</string>\n      <key>ProgramArguments</key>\n      <array>\n      <string>/Users/paul/tavern/bin/python3.5</string>\n      <string>-c</string>\n      <string>{}</string>\n      </array>\n      <key>UserName</key>\n      <string>%s</string>\n      <key>StandardOutPath</key>\n      <string>{}</string>\n      <key>StandardErrorPath</key>\n      <string>{}</string>\n      <key>KeepAlive</key>\n      <true/>\n  </dict>\n  </plist>\n  '%(getuser())
    title = "%s"%([exec("import nltk",globals()),random.sample(random.sample(list(nltk.wordnet.wordnet.all_synsets(nltk.wordnet.wordnet.NOUN)),1)[0].lemmas(),1)[0].name()][1])
    os.makedirs(userfolder("~/tavern/tavern/soda/plists"),exist_ok=True)
    save_path = userfolder("~/tavern/tavern/soda/plists/%s.plist"%(title))
    y = 'import os; os.chdir(os.path.expanduser("~/tavern/tavern")); from soda.can import *; %s'%(x)
    x = r.format(save_path.split("/")[-1].split(".")[0],y,save_path+".out",save_path+".err").strip().replace("\n  ", "\n")
    open(save_path, "w").write(x)
    return x
  globals().update(locals())
class Firefox_Porter:
  def __init__(self, io = None):
    if os.path.exists(io):
      rm(GLOBAL_FIREFOX_PROFILE_PATH)
      os.makedirs(GLOBAL_FIREFOX_PROFILE_PATH, exist_ok = False)
      lmap(lambda i: os.system("/Applications/Firefox\ 46.app/Contents/MacOS/firefox-bin -CreateProfile %s" % i), lmap(lambda i: i.split(".")[-1], os.listdir(io)))
      lmap(lambda i: os.system("rm -rf %s"%(Join("/",address_backslash(GLOBAL_FIREFOX_PROFILE_PATH),i,"*"))), os.listdir(GLOBAL_FIREFOX_PROFILE_PATH))
      lmap(lambda i: os.system("cp -r %s %s" % (Join("/", io, i, "*"),Join("/",address_backslash(GLOBAL_FIREFOX_PROFILE_PATH),[j for j in os.listdir(GLOBAL_FIREFOX_PROFILE_PATH) if j.split(".")[-1]==i.split(".")[-1]][0],""))), os.listdir(io))
    else:
      io = (lmap(lambda i: i.split(".")[-1], os.listdir(GLOBAL_FIREFOX_PROFILE_PATH)))if(io==None)else(io)
      io = lmap(lambda i: [j for j in os.listdir(GLOBAL_FIREFOX_PROFILE_PATH) if j.split(".")[-1]==i][0], io)
      os.makedirs("Firefox_Port", exist_ok = False)
      lmap(lambda i: os.system("cp -r '%s' '%s'" % (Join("/",GLOBAL_FIREFOX_PROFILE_PATH,i),Join("/","Firefox_Port",i))), io)
      zipUtil("Firefox_Port")
    """
    Firefox_Porter(io = None) # Port Out
    redprint("\n".join(os.listdir("Firefox_Port")))
    Firefox_Porter("Firefox_Port") # Port In

    Firefox_Porter(io = ["sele2", "main_panels", "emails", "default"]) # Port One
    redprint("\n".join(os.listdir("Firefox_Port")))
    Firefox_Porter("Firefox_Port") # Port In
    """
class Firefox_Profile:
  def __init__(self, profile):
    [rm(Join("/", GLOBAL_FIREFOX_PROFILE_PATH, i)) for i in os.listdir(GLOBAL_FIREFOX_PROFILE_PATH) if i.split(".")[-1] == profile]
    os.system("/Applications/Firefox\ 46.app/Contents/MacOS/firefox-bin -CreateProfile %s" % (profile))
    R = [i for i in os.listdir(GLOBAL_FIREFOX_PROFILE_PATH) if i.split(".")[-1] == profile][0]
    # open(Join("/", GLOBAL_FIREFOX_PROFILE_PATH, R, "prefs.js"), "w").write('// Mozilla User Preferences\n\n// DO NOT EDIT THIS FILE.\n//\n// If you make changes to this file while the application is running,\n// the changes will be overwritten when the application exits.\n//\n// To change a preference value, you can either:\n// - modify it via the UI (e.g. via about:config in the browser); or\n// - set it within a user.js file in your profile.\n\nuser_pref("app.normandy.first_run", false);\nuser_pref("app.normandy.user_id", "06ce59be-456c-b540-9a47-0941c6043180");\nuser_pref("app.update.auto", false);\nuser_pref("app.update.enabled", false);\nuser_pref("app.update.lastUpdateTime.addon-background-update-timer", 0);\nuser_pref("app.update.lastUpdateTime.background-update-timer", 1550635354);\nuser_pref("app.update.lastUpdateTime.blocklist-background-update-timer", 0);\nuser_pref("app.update.lastUpdateTime.browser-cleanup-thumbnails", 1550633597);\nuser_pref("app.update.lastUpdateTime.recipe-client-addon-run", 0);\nuser_pref("app.update.lastUpdateTime.search-engine-update-timer", 1550635039);\nuser_pref("app.update.lastUpdateTime.services-settings-poll-changes", 1550635420);\nuser_pref("app.update.lastUpdateTime.telemetry_modules_ping", 0);\nuser_pref("app.update.lastUpdateTime.xpi-signature-verification", 0);\nuser_pref("browser.bookmarks.restore_default_bookmarks", false);\nuser_pref("browser.cache.disk.capacity", 1048576);\nuser_pref("browser.cache.disk.filesystem_reported", 1);\nuser_pref("browser.cache.disk.smart_size.first_run", false);\nuser_pref("browser.cache.disk.smart_size.use_old_max", false);\nuser_pref("browser.cache.frecency_experiment", 1);\nuser_pref("browser.contentblocking.category", "standard");\nuser_pref("browser.download.importedFromSqlite", true);\nuser_pref("browser.laterrun.bookkeeping.profileCreationTime", 1550633567);\nuser_pref("browser.laterrun.bookkeeping.sessionCount", 12);\nuser_pref("browser.laterrun.enabled", true);\nuser_pref("browser.migrated-sync-button", true);\nuser_pref("browser.migration.version", 77);\nuser_pref("browser.newtabpage.activity-stream.feeds.section.highlights", false);\nuser_pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);\nuser_pref("browser.newtabpage.activity-stream.feeds.section.topstories.rec.impressions", "{"34054":1550633569243,"34079":1550633569243,"34084":1550633569243}");\nuser_pref("browser.newtabpage.activity-stream.feeds.section.topstories.spoc.impressions", "{"787":[1550634723461,1550634727923,1550634732355],"1099":[1550635011420]}");\nuser_pref("browser.newtabpage.activity-stream.feeds.snippets", false);\nuser_pref("browser.newtabpage.activity-stream.feeds.topsites", false);\nuser_pref("browser.newtabpage.activity-stream.impressionId", "{c85341b3-f663-9243-bac9-83b8e7427423}");\nuser_pref("browser.newtabpage.activity-stream.migrationLastShownDate", 1550552400);\nuser_pref("browser.newtabpage.activity-stream.migrationRemainingDays", 3);\nuser_pref("browser.newtabpage.activity-stream.prerender", false);\nuser_pref("browser.newtabpage.activity-stream.section.highlights.includeBookmarks", false);\nuser_pref("browser.newtabpage.activity-stream.section.highlights.includeDownloads", false);\nuser_pref("browser.newtabpage.activity-stream.section.highlights.includePocket", false);\nuser_pref("browser.newtabpage.activity-stream.section.highlights.includeVisited", false);\nuser_pref("browser.newtabpage.activity-stream.showSearch", false);\nuser_pref("browser.newtabpage.activity-stream.showSponsored", false);\nuser_pref("browser.newtabpage.enhanced", true);\nuser_pref("browser.newtabpage.storageVersion", 1);\nuser_pref("browser.pageActions.persistedActions", "{"version":1,"ids":["bookmark","bookmarkSeparator","copyURL","emailLink","addSearchEngine","sendToDevice","shareURL","pocket","screenshots_mozilla_org"],"idsInUrlbar":["pocket","bookmark"]}");\nuser_pref("browser.pagethumbnails.storage_version", 3);\nuser_pref("browser.places.smartBookmarksVersion", 7);\nuser_pref("browser.preferences.advanced.selectedTabIndex", 0);\nuser_pref("browser.rights.3.shown", true);\nuser_pref("browser.safebrowsing.provider.google4.lastupdatetime", "1550635400587");\nuser_pref("browser.safebrowsing.provider.google4.nextupdatetime", "1550637198587");\nuser_pref("browser.safebrowsing.provider.mozilla.lastupdatetime", "1550633571752");\nuser_pref("browser.safebrowsing.provider.mozilla.nextupdatetime", "1550637171752");\nuser_pref("browser.search.cohort", "nov17-2");\nuser_pref("browser.search.countryCode", "US");\nuser_pref("browser.search.region", "US");\nuser_pref("browser.sessionstore.upgradeBackup.latestBuildID", "20190211233335");\nuser_pref("browser.shell.checkDefaultBrowser", false);\nuser_pref("browser.shell.didSkipDefaultBrowserCheckOnFirstRun", true);\nuser_pref("browser.slowStartup.averageTime", 855);\nuser_pref("browser.slowStartup.samples", 1);\nuser_pref("browser.startup.homepage_override.buildID", "20190211233335");\nuser_pref("browser.startup.homepage_override.mstone", "65.0.1");\nuser_pref("browser.uiCustomization.state", "{"placements":{"widget-overflow-fixed-list":[],"nav-bar":["back-button","forward-button","stop-reload-button","home-button","customizableui-special-spring1","urlbar-container","customizableui-special-spring2","downloads-button","library-button","sidebar-button","loop-button"],"TabsToolbar":["tabbrowser-tabs","new-tab-button","alltabs-button"],"PersonalToolbar":["personal-bookmarks"]},"seen":["developer-button","loop-button","pocket-button","feed-button"],"dirtyAreaCache":["nav-bar","TabsToolbar","PersonalToolbar"],"currentVersion":15,"newElementCount":2}");\nuser_pref("browser.urlbar.placeholderName", "Google");\nuser_pref("browser.urlbar.timesBeforeHidingSuggestionsHint", 2);\nuser_pref("datareporting.healthreport.uploadEnabled", false);\nuser_pref("datareporting.policy.dataSubmissionPolicyAcceptedVersion", 2);\nuser_pref("datareporting.policy.dataSubmissionPolicyNotifiedTime", "1550633570624");\nuser_pref("datareporting.sessions.current.activeTicks", 7);\nuser_pref("datareporting.sessions.current.clean", true);\nuser_pref("datareporting.sessions.current.firstPaint", 664);\nuser_pref("datareporting.sessions.current.main", 73);\nuser_pref("datareporting.sessions.current.sessionRestored", 2511);\nuser_pref("datareporting.sessions.current.startTime", "1550633939369");\nuser_pref("datareporting.sessions.current.totalTime", 37);\nuser_pref("devtools.onboarding.telemetry.logged", true);\nuser_pref("distribution.iniFile.exists.appversion", "65.0.1");\nuser_pref("distribution.iniFile.exists.value", false);\nuser_pref("dom.apps.reset-permissions", true);\nuser_pref("dom.forms.autocomplete.formautofill", true);\nuser_pref("dom.mozApps.used", true);\nuser_pref("e10s.rollout.cohort", "unsupportedChannel");\nuser_pref("experiments.activeExperiment", false);\nuser_pref("extensions.blocklist.pingCountVersion", -1);\nuser_pref("extensions.bootstrappedAddons", "{"firefox@getpocket.com":{"version":"1.0","type":"extension","descriptor":"/Applications/Firefox.app/Contents/Resources/browser/features/firefox@getpocket.com.xpi","multiprocessCompatible":false,"runInSafeMode":true},"loop@mozilla.org":{"version":"1.2.6","type":"extension","descriptor":"/Applications/Firefox.app/Contents/Resources/browser/features/loop@mozilla.org.xpi","multiprocessCompatible":false,"runInSafeMode":true},"e10srollout@mozilla.org":{"version":"1.0","type":"extension","descriptor":"/Applications/Firefox.app/Contents/Resources/browser/features/e10srollout@mozilla.org.xpi","multiprocessCompatible":false,"runInSafeMode":true}}");\nuser_pref("extensions.databaseSchema", 28);\nuser_pref("extensions.e10sBlockedByAddons", false);\nuser_pref("extensions.enabledAddons", "%7B972ce4c6-7e08-4474-a285-3208198ce6fd%7D:46.0");\nuser_pref("extensions.getAddons.cache.lastUpdate", 1550633941);\nuser_pref("extensions.getAddons.databaseSchema", 5);\nuser_pref("extensions.lastAppBuildId", "20190211233335");\nuser_pref("extensions.lastAppVersion", "65.0.1");\nuser_pref("extensions.lastPlatformVersion", "65.0.1");\nuser_pref("extensions.pendingOperations", false);\nuser_pref("extensions.systemAddonSet", "{"schema":1,"addons":{}}");\nuser_pref("extensions.webcompat.perform_injections", true);\nuser_pref("extensions.webcompat.perform_ua_overrides", true);\nuser_pref("extensions.webextensions.uuids", "{"formautofill@mozilla.org":"2b4f0ede-b4d9-6545-9ac0-e1660f03296f","screenshots@mozilla.org":"a1a637bf-7c5f-f446-908f-d12e4f77d811","webcompat-reporter@mozilla.org":"9bf34646-9ad4-954f-9c4e-1063d8c70d25","webcompat@mozilla.org":"b79d04e0-3f7f-3b44-a76a-3cdbecb89a81"}");\nuser_pref("extensions.xpiState", "{"app-system-defaults":{"firefox@getpocket.com":{"d":"/Applications/Firefox.app/Contents/Resources/browser/features/firefox@getpocket.com.xpi","e":true,"v":"1.0","st":1540071218000},"loop@mozilla.org":{"d":"/Applications/Firefox.app/Contents/Resources/browser/features/loop@mozilla.org.xpi","e":true,"v":"1.2.6","st":1540071218000},"e10srollout@mozilla.org":{"d":"/Applications/Firefox.app/Contents/Resources/browser/features/e10srollout@mozilla.org.xpi","e":true,"v":"1.0","st":1540071218000}},"app-global":{"{972ce4c6-7e08-4474-a285-3208198ce6fd}":{"d":"/Applications/Firefox.app/Contents/Resources/browser/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}.xpi","e":true,"v":"46.0","st":1540071218000}}}");\nuser_pref("font.internaluseonly.changed", true);\nuser_pref("gecko.buildID", "20160421124000");\nuser_pref("gecko.mstone", "46.0");\nuser_pref("lightweightThemes.persisted.headerURL", false);\nuser_pref("lightweightThemes.usedThemes", "[]");\nuser_pref("media.gmp.storage.version.observed", 1);\nuser_pref("network.cookie.prefsMigrated", true);\nuser_pref("network.predictor.cleaned-up", true);\nuser_pref("pdfjs.enabledCache.state", false);\nuser_pref("pdfjs.migrationVersion", 2);\nuser_pref("pdfjs.previousHandler.alwaysAskBeforeHandling", true);\nuser_pref("pdfjs.previousHandler.preferredAction", 4);\nuser_pref("places.history.expiration.transient_current_max_pages", 112348);\nuser_pref("plugin.disable_full_page_plugin_for_types", "application/pdf");\nuser_pref("privacy.cpd.offlineApps", true);\nuser_pref("privacy.cpd.siteSettings", true);\nuser_pref("privacy.sanitize.migrateClearSavedPwdsOnExit", true);\nuser_pref("privacy.sanitize.pending", "[{"id":"newtab-container","itemsToClear":[],"options":{}}]");\nuser_pref("privacy.sanitize.timeSpan", 0);\nuser_pref("security.sandbox.content.tempDirSuffix", "d0b0a17d-ddae-9c44-bb41-7cfca103ccd5");\nuser_pref("security.sandbox.plugin.tempDirSuffix", "9ad5aae9-5dc2-ac4f-9263-0195647a6ab7");\nuser_pref("services.blocklist.addons.checked", 1550635565);\nuser_pref("services.blocklist.onecrl.checked", 1550635565);\nuser_pref("services.blocklist.plugins.checked", 1550635565);\nuser_pref("services.settings.clock_skew_seconds", -145);\nuser_pref("services.settings.last_update_seconds", 1550635565);\nuser_pref("services.settings.main.language-dictionaries.last_check", 1550635565);\nuser_pref("services.settings.main.onboarding.last_check", 1550635565);\nuser_pref("services.settings.main.sites-classification.last_check", 1550635565);\nuser_pref("services.sync.clients.lastSync", "0");\nuser_pref("services.sync.clients.lastSyncLocal", "0");\nuser_pref("services.sync.declinedEngines", "");\nuser_pref("services.sync.engine.addresses.available", true);\nuser_pref("services.sync.globalScore", 0);\nuser_pref("services.sync.migrated", true);\nuser_pref("services.sync.nextSync", 0);\nuser_pref("services.sync.tabs.lastSync", "0");\nuser_pref("services.sync.tabs.lastSyncLocal", "0");\nuser_pref("signon.importedFromSqlite", true);\nuser_pref("toolkit.startup.last_success", 1550635390);\nuser_pref("toolkit.telemetry.cachedClientID", "c0ffeec0-ffee-c0ff-eec0-ffeec0ffeec0");\nuser_pref("toolkit.telemetry.previousBuildID", "20190211233335");\nuser_pref("toolkit.telemetry.reportingpolicy.firstRun", false);\n')
    open(Join("/", GLOBAL_FIREFOX_PROFILE_PATH, R, "prefs.js"), "w").write('// Mozilla User Preferences\n\n// DO NOT EDIT THIS FILE.\n//\n// If you make changes to this file while the application is running,\n// the changes will be overwritten when the application exits.\n//\n// To change a preference value, you can either:\n// - modify it via the UI (e.g. via about:config in the browser); or\n// - set it within a user.js file in your profile.\n\nuser_pref("app.normandy.first_run", false);\nuser_pref("app.normandy.user_id", "06ce59be-456c-b540-9a47-0941c6043180");\nuser_pref("app.update.auto", false);\nuser_pref("app.update.elevate.version", "66.0.3");\nuser_pref("app.update.enabled", false);\nuser_pref("app.update.lastUpdateTime.addon-background-update-timer", 1553728744);\nuser_pref("app.update.lastUpdateTime.background-update-timer", 1550635354);\nuser_pref("app.update.lastUpdateTime.blocklist-background-update-timer", 1553728915);\nuser_pref("app.update.lastUpdateTime.browser-cleanup-thumbnails", 1550633597);\nuser_pref("app.update.lastUpdateTime.recipe-client-addon-run", 0);\nuser_pref("app.update.lastUpdateTime.search-engine-update-timer", 1550635039);\nuser_pref("app.update.lastUpdateTime.services-settings-poll-changes", 1550635420);\nuser_pref("app.update.lastUpdateTime.telemetry_modules_ping", 0);\nuser_pref("app.update.lastUpdateTime.xpi-signature-verification", 1553729321);\nuser_pref("app.update.silent", true);\nuser_pref("app.update.url", "xxxhttps://xxxaus5.mozilla.org/update/6/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%SYSTEM_CAPABILITIES%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/update.xml");\nuser_pref("browser.bookmarks.restore_default_bookmarks", false);\nuser_pref("browser.cache.disk.capacity", 1048576);\nuser_pref("browser.cache.disk.filesystem_reported", 1);\nuser_pref("browser.cache.disk.smart_size.first_run", false);\nuser_pref("browser.cache.disk.smart_size.use_old_max", false);\nuser_pref("browser.cache.frecency_experiment", 1);\nuser_pref("browser.contentblocking.category", "standard");\nuser_pref("browser.ctrlTab.recentlyUsedOrder", false);\nuser_pref("browser.download.importedFromSqlite", true);\nuser_pref("browser.laterrun.bookkeeping.profileCreationTime", 1550633567);\nuser_pref("browser.laterrun.bookkeeping.sessionCount", 13);\nuser_pref("browser.migrated-sync-button", true);\nuser_pref("browser.migration.version", 77);\nuser_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr", false);\nuser_pref("browser.newtabpage.activity-stream.feeds.section.highlights", false);\nuser_pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);\nuser_pref("browser.newtabpage.activity-stream.feeds.snippets", false);\nuser_pref("browser.newtabpage.activity-stream.feeds.topsites", false);\nuser_pref("browser.newtabpage.activity-stream.impressionId", "{c85341b3-f663-9243-bac9-83b8e7427423}");\nuser_pref("browser.newtabpage.activity-stream.migrationExpired", true);\nuser_pref("browser.newtabpage.activity-stream.migrationLastShownDate", 1553659200);\nuser_pref("browser.newtabpage.activity-stream.migrationRemainingDays", 2);\nuser_pref("browser.newtabpage.activity-stream.prerender", false);\nuser_pref("browser.newtabpage.activity-stream.section.highlights.includeBookmarks", false);\nuser_pref("browser.newtabpage.activity-stream.section.highlights.includeDownloads", false);\nuser_pref("browser.newtabpage.activity-stream.section.highlights.includePocket", false);\nuser_pref("browser.newtabpage.activity-stream.section.highlights.includeVisited", false);\nuser_pref("browser.newtabpage.activity-stream.showSearch", false);\nuser_pref("browser.newtabpage.activity-stream.showSponsored", false);\nuser_pref("browser.newtabpage.enabled", false);\nuser_pref("browser.newtabpage.enhanced", true);\nuser_pref("browser.newtabpage.storageVersion", 1);\nuser_pref("browser.pageActions.persistedActions", "{"version":1,"ids":["bookmark","bookmarkSeparator","copyURL","emailLink","addSearchEngine","sendToDevice","shareURL","pocket"],"idsInUrlbar":["pocket","bookmark"]}");\nuser_pref("browser.pagethumbnails.storage_version", 3);\nuser_pref("browser.places.smartBookmarksVersion", 7);\nuser_pref("browser.preferences.advanced.selectedTabIndex", 0);\nuser_pref("browser.preferences.defaultPerformanceSettings.enabled", false);\nuser_pref("browser.rights.3.shown", true);\nuser_pref("browser.safebrowsing.provider.google4.lastupdatetime", "1557288602301");\nuser_pref("browser.safebrowsing.provider.google4.nextupdatetime", "1557290413301");\nuser_pref("browser.safebrowsing.provider.mozilla.lastupdatetime", "1557288602720");\nuser_pref("browser.safebrowsing.provider.mozilla.nextupdatetime", "1557292202720");\nuser_pref("browser.search.cohort", "nov17-2");\nuser_pref("browser.search.countryCode", "US");\nuser_pref("browser.search.hiddenOneOffs", "Google,Bing,Amazon.com,DuckDuckGo,eBay,Twitter,Wikipedia (en)");\nuser_pref("browser.search.region", "US");\nuser_pref("browser.search.suggest.enabled", false);\nuser_pref("browser.sessionstore.upgradeBackup.latestBuildID", "20190211233335");\nuser_pref("browser.shell.checkDefaultBrowser", false);\nuser_pref("browser.shell.didSkipDefaultBrowserCheckOnFirstRun", true);\nuser_pref("browser.slowStartup.averageTime", 975);\nuser_pref("browser.slowStartup.samples", 1);\nuser_pref("browser.startup.homepage", "about:blank");\nuser_pref("browser.startup.homepage_override.buildID", "20190124174741");\nuser_pref("browser.startup.homepage_override.mstone", "65.0");\nuser_pref("browser.uiCustomization.state", "{"placements":{"widget-overflow-fixed-list":[],"nav-bar":["back-button","forward-button","stop-reload-button","home-button","customizableui-special-spring1","urlbar-container","customizableui-special-spring2","downloads-button","library-button","sidebar-button"],"TabsToolbar":["tabbrowser-tabs","new-tab-button","alltabs-button"],"PersonalToolbar":["personal-bookmarks"]},"seen":["developer-button"],"dirtyAreaCache":["nav-bar"],"currentVersion":15,"newElementCount":2}");\nuser_pref("browser.urlbar.placeholderName", "Google");\nuser_pref("browser.urlbar.searchSuggestionsChoice", false);\nuser_pref("browser.urlbar.suggest.bookmark", false);\nuser_pref("browser.urlbar.suggest.openpage", false);\nuser_pref("browser.urlbar.suggest.searches", false);\nuser_pref("browser.urlbar.timesBeforeHidingSuggestionsHint", 1);\nuser_pref("datareporting.healthreport.uploadEnabled", false);\nuser_pref("datareporting.policy.dataSubmissionPolicyAcceptedVersion", 2);\nuser_pref("datareporting.policy.dataSubmissionPolicyNotifiedTime", "1550633570624");\nuser_pref("datareporting.sessions.current.activeTicks", 7);\nuser_pref("datareporting.sessions.current.clean", true);\nuser_pref("datareporting.sessions.current.firstPaint", 664);\nuser_pref("datareporting.sessions.current.main", 73);\nuser_pref("datareporting.sessions.current.sessionRestored", 2511);\nuser_pref("datareporting.sessions.current.startTime", "1550633939369");\nuser_pref("datareporting.sessions.current.totalTime", 37);\nuser_pref("devtools.onboarding.telemetry.logged", true);\nuser_pref("distribution.iniFile.exists.appversion", "65.0");\nuser_pref("distribution.iniFile.exists.value", false);\nuser_pref("dom.apps.reset-permissions", true);\nuser_pref("dom.forms.autocomplete.formautofill", true);\nuser_pref("dom.mozApps.used", true);\nuser_pref("e10s.rollout.cohort", "unsupportedChannel");\nuser_pref("experiments.activeExperiment", false);\nuser_pref("extensions.blocklist.lastModified", "Tue, 26 Mar 2019 17:13:55 GMT");\nuser_pref("extensions.blocklist.pingCountVersion", -1);\nuser_pref("extensions.databaseSchema", 28);\nuser_pref("extensions.e10sBlockedByAddons", false);\nuser_pref("extensions.enabledAddons", "%7B972ce4c6-7e08-4474-a285-3208198ce6fd%7D:46.0");\nuser_pref("extensions.getAddons.cache.lastUpdate", 1553728744);\nuser_pref("extensions.getAddons.databaseSchema", 5);\nuser_pref("extensions.lastAppBuildId", "20190124174741");\nuser_pref("extensions.lastAppVersion", "65.0");\nuser_pref("extensions.lastPlatformVersion", "65.0");\nuser_pref("extensions.pendingOperations", false);\nuser_pref("extensions.webcompat.perform_injections", true);\nuser_pref("extensions.webcompat.perform_ua_overrides", true);\nuser_pref("extensions.webextensions.uuids", "{"formautofill@mozilla.org":"fd82627d-7029-df44-854c-65997238f507","screenshots@mozilla.org":"1b26d190-485a-3a41-991d-cbdbedab016b","webcompat-reporter@mozilla.org":"cdb30fdf-9916-544d-9ae5-be2506ea93c1","webcompat@mozilla.org":"f3f59ad4-5a24-054e-9a2d-8807fc628a8e"}");\nuser_pref("font.internaluseonly.changed", false);\nuser_pref("gecko.buildID", "20160421124000");\nuser_pref("gecko.mstone", "46.0");\nuser_pref("layers.acceleration.disabled", true);\nuser_pref("lightweightThemes.persisted.headerURL", false);\nuser_pref("lightweightThemes.usedThemes", "[]");\nuser_pref("media.gmp.storage.version.observed", 1);\nuser_pref("network.cookie.prefsMigrated", true);\nuser_pref("network.predictor.cleaned-up", true);\nuser_pref("pdfjs.enabledCache.state", false);\nuser_pref("pdfjs.migrationVersion", 2);\nuser_pref("pdfjs.previousHandler.alwaysAskBeforeHandling", true);\nuser_pref("pdfjs.previousHandler.preferredAction", 4);\nuser_pref("places.history.expiration.transient_current_max_pages", 112348);\nuser_pref("plugin.disable_full_page_plugin_for_types", "application/pdf");\nuser_pref("privacy.cpd.offlineApps", true);\nuser_pref("privacy.cpd.siteSettings", true);\nuser_pref("privacy.sanitize.migrateClearSavedPwdsOnExit", true);\nuser_pref("privacy.sanitize.pending", "[]");\nuser_pref("privacy.sanitize.timeSpan", 0);\nuser_pref("security.sandbox.content.tempDirSuffix", "d0b0a17d-ddae-9c44-bb41-7cfca103ccd5");\nuser_pref("security.sandbox.plugin.tempDirSuffix", "9ad5aae9-5dc2-ac4f-9263-0195647a6ab7");\nuser_pref("services.blocklist.addons.checked", 1550635565);\nuser_pref("services.blocklist.onecrl.checked", 1550635565);\nuser_pref("services.blocklist.plugins.checked", 1550635565);\nuser_pref("services.settings.clock_skew_seconds", -145);\nuser_pref("services.settings.last_update_seconds", 1550635565);\nuser_pref("services.settings.main.language-dictionaries.last_check", 1550635565);\nuser_pref("services.settings.main.onboarding.last_check", 1550635565);\nuser_pref("services.settings.main.sites-classification.last_check", 1550635565);\nuser_pref("services.sync.clients.lastSync", "0");\nuser_pref("services.sync.clients.lastSyncLocal", "0");\nuser_pref("services.sync.declinedEngines", "");\nuser_pref("services.sync.engine.addresses.available", true);\nuser_pref("services.sync.globalScore", 0);\nuser_pref("services.sync.migrated", true);\nuser_pref("services.sync.nextSync", 0);\nuser_pref("services.sync.tabs.lastSync", "0");\nuser_pref("services.sync.tabs.lastSyncLocal", "0");\nuser_pref("signon.importedFromSqlite", true);\nuser_pref("signon.rememberSignons", false);\nuser_pref("toolkit.startup.last_success", 1557288598);\nuser_pref("toolkit.telemetry.cachedClientID", "c0ffeec0-ffee-c0ff-eec0-ffeec0ffeec0");\nuser_pref("toolkit.telemetry.previousBuildID", "20190124174741");\nuser_pref("toolkit.telemetry.reportingpolicy.firstRun", false);\n')
    Binarydata().export("places.sqlite", Join("/", GLOBAL_FIREFOX_PROFILE_PATH, R, "places.sqlite"))
class Menulets:
  class Fig:
    def __init__(self):
      import rumps
      from rumps import MenuItem as M
      from rumps import MenuItem
      self.app = rumps.App("🍃", quit_button=Null)
      globals().update(locals())


      self.set_menu()
      time.sleep(3.2)
      # process(lambda: [[time.sleep(1),[self.set_menu(),Update(All(Muta)[0],fig_changed=0)] if All(Muta)[0].fig_changed == 1 else()] for i in range(WHILE_TRUE)])
      time.sleep(0)
      self.app.run()

    def set_menu(self):
      keys = list(self.app.menu.keys())
      redprint(keys)
      for i in keys:
        self.app.menu.pop(i)
      self.app.title = "|%s|%s|%s|%s|%s|"%(Muta()().store_abbre.upper()if(Muta()().store_abbre)else("-"), (Muta()().niche)if(Muta()().niche)else("-"), (Muta()().add_thumbnails)if(Muta()().add_thumbnails)else("-"),(Muta()().is_free_plus_ship)if(Muta()().is_free_plus_ship)else("-"),(Muta()().page)if(Muta()().page)else("-"), )
      self.app.menu = [

                  ]
  class Handles:
    # Basically, it shows the day's sales for all shops, as well and if clicked, shows the adsets.
    def __init__(self):
      import rumps
      from rumps import MenuItem as M
      from rumps import MenuItem
      self.app = rumps.App("🚀",quit_button=Null)
      globals().update(locals())


      self.set_menu()
      #process(  lambda: [time.sleep(6.15), self.set_menu()]  )
      time.sleep(6)
      self.app.run()


    def set_menu(self):
      keys = list(self.app.menu.keys())
      redprint(keys)
      for i in keys:
        self.app.menu.pop(i)
      keycall("Icon",All(Adset))
      keycall("post_handle",All(Adset))
      self.app.menu = [MenuItem("/",callback=lambda _=None:[keycall("post_handle",All(Adset)),keycall("__call__",All(Handle)),self.set_menu()])]+\
                      [
                        MenuItem("[%s]"%(i.reach),icon=Filter(Adset,handle=i.handle)[0].Icon()) for i in keysort("reach",All(Handle),tcer=True)
                      ]
  class Menulet_Timer:
    def __init__(self):
      """
      Stepone: ^--
      Drofdown: Repeat_Setting|Yeah
      """
      import rumps
      from rumps import MenuItem as M
      from rumps import MenuItem
      self.app = rumps.App("0:00",quit_button=Null)
      globals().update(locals())


      self.is_repeat = False
      self.set_menu()
      time.sleep(6)
      self.app.run()


    def set_menu(self):
      keys = list(self.app.menu.keys())
      redprint(keys)
      for i in keys:
        self.app.menu.pop(i)
      self.notify=False
      self.app.menu = [
                        MenuItem("Is_Repeat %s"%("On"if(self.is_repeat)else("Off")),callback=lambda _=None:[setattr(self,"is_repeat",not self.is_repeat),self.set_menu()]),
                        MenuItem("1:00",callback=lambda _=None:process(lambda: [[[setattr(self.app,"title","%s:%s" % (int((60-i)/60), str((60-i)%60).zfill(2) )),zz(1)] for i in range(61)] for i in range(1 if self.is_repeat == False else WHILE_TRUE)])),
                        MenuItem("2:00",callback=lambda _=None:process(lambda: [[[setattr(self.app,"title","%s:%s" % (int((120-i)/60), str((120-i)%60).zfill(2) )),OSA.notify("%s:%s" % (int((120-i)/60), str((120-i)%60).zfill(2) )) if self.notify == 1 else(),zz(1)] for i in range(121)] for i in range(1 if self.is_repeat == False else WHILE_TRUE)])),
                        MenuItem("4:00",callback=lambda _=None:process(lambda: [[[setattr(self.app,"title","%s:%s" % (int((240-i)/60), str((240-i)%60).zfill(2) )),OSA.notify("%s:%s" % (int((240-i)/60), str((240-i)%60).zfill(2) )) if self.notify == 1 else(),zz(1)] for i in range(241)] for i in range(1 if self.is_repeat == False else WHILE_TRUE)])),
                        MenuItem("10:00",callback=lambda _=None:process(lambda: [[[setattr(self.app,"title","%s:%s" % (int((600-i)/60), str((600-i)%60).zfill(2) )),OSA.notify("%s:%s" % (int((600-i)/60), str((600-i)%60).zfill(2) )) if self.notify == 1 else(),zz(1)] for i in range(601)] for i in range(1 if self.is_repeat == False else WHILE_TRUE)])),
                        MenuItem("Set Timer", callback = lambda _=None: process(lambda: [globalise(datetime.strptime(OSA.display_dialog("Alarm Timer? In format Day of week, Hour of day, Minute of the hour, AM/PM")+ (", ") + ("%s, %s, %s"%(datetime.now().year,datetime.now().month,datetime.now().day)),"%A, %I, %M, %p, %Y, %m, %d"),"menulet_timer_alarm"),[[([[os.system("osascript -e 'set Volume 10'"),os.system("afplay /System/Library/Sounds/Submarine.aiff -v 10 &"),time.sleep(0.5)] for i in range(WHILE_TRUE)]) if( ((globe("menulet_timer_alarm").weekday()==datetime.now().weekday())and(globe("menulet_timer_alarm").hour==datetime.now().hour)and(globe("menulet_timer_alarm").minute==datetime.now().minute)) )else(),time.sleep(30)] for i in range(WHILE_TRUE)],self.set_menu()])),
                      ]
      self.app.menu = [[1, [
                        MenuItem("Is_Repeat %s"%("On"if(self.is_repeat)else("Off")),callback=lambda _=None:[setattr(self,"is_repeat",not self.is_repeat),self.set_menu()]),
                        MenuItem("1:00",callback=lambda _=None:process(lambda: [[[setattr(self.app,"title","%s:%s" % (int((60-i)/60), str((60-i)%60).zfill(2) )),zz(1)] for i in range(61)] for i in range(1 if self.is_repeat == False else WHILE_TRUE)])),
                        MenuItem("2:00",callback=lambda _=None:process(lambda: [[[setattr(self.app,"title","%s:%s" % (int((120-i)/60), str((120-i)%60).zfill(2) )),OSA.notify("%s:%s" % (int((120-i)/60), str((120-i)%60).zfill(2) )) if self.notify == 1 else(),zz(1)] for i in range(121)] for i in range(1 if self.is_repeat == False else WHILE_TRUE)])),
                        MenuItem("4:00",callback=lambda _=None:process(lambda: [[[setattr(self.app,"title","%s:%s" % (int((240-i)/60), str((240-i)%60).zfill(2) )),OSA.notify("%s:%s" % (int((240-i)/60), str((240-i)%60).zfill(2) )) if self.notify == 1 else(),zz(1)] for i in range(241)] for i in range(1 if self.is_repeat == False else WHILE_TRUE)])),
                        MenuItem("10:00",callback=lambda _=None:process(lambda: [[[setattr(self.app,"title","%s:%s" % (int((600-i)/60), str((600-i)%60).zfill(2) )),OSA.notify("%s:%s" % (int((600-i)/60), str((600-i)%60).zfill(2) )) if self.notify == 1 else(),zz(1)] for i in range(601)] for i in range(1 if self.is_repeat == False else WHILE_TRUE)])),
                        MenuItem("Set Timer", callback = lambda _=None: process(lambda: [globalise(datetime.strptime(OSA.display_dialog("Alarm Timer? In format Day of week, Hour of day, Minute of the hour, AM/PM")+ (", ") + ("%s, %s, %s"%(datetime.now().year,datetime.now().month,datetime.now().day)),"%A, %I, %M, %p, %Y, %m, %d"),"menulet_timer_alarm"),[[([[os.system("osascript -e 'set Volume 10'"),os.system("afplay /System/Library/Sounds/Submarine.aiff -v 10 &"),time.sleep(0.5)] for i in range(WHILE_TRUE)]) if( ((globe("menulet_timer_alarm").weekday()==datetime.now().weekday())and(globe("menulet_timer_alarm").hour==datetime.now().hour)and(globe("menulet_timer_alarm").minute==datetime.now().minute)) )else(),time.sleep(30)] for i in range(WHILE_TRUE)],self.set_menu()])),
                      ]]]
  class Nemulet:
    def __call__(self):
      os.system("cd ~/tavern/tavern && ~/tavern/bin/python3.5 -c 'from soda.can import *; Nemulet().results()' &")
      os.system("cd ~/tavern/tavern && ~/tavern/bin/python3.5 -c 'from soda.can import *; Nemulet().suggestions()' &")
      os.system("cd ~/tavern/tavern && ~/tavern/bin/python3.5 -c 'from soda.can import *; Nemulet().interest_box()' &")
    def change_mutaliskconfig_title(self):
      x = OSA().display_dialog("Title|image_url?: ")
      #x = pyperclip.paste()
      x.split("|") # in case you pressed the hotkeys by accident, it will erried here.
      title, image_url = x.split("|")
      a = Muta.objects.all()[0]
      a.title = title;
      a.image_url = image_url;
      setattr(a,"amplitude",-1)
      a.save() #;;
      OSA().notify("spear - ")
      #assert Muta.objects.all()[0].title == title
      #assert Muta.objects.all()[0].image_url == image_url
      #Nemulet().interest_box_spear()
    @staticmethod
    def change_mutaliskconfig_store():    Update(Muta.objects.all()[0],         store_abbre=  OSA.display_dialog("🎪", dropdown_options=[i.shop_abbreviation for i in keysort("shop_abbreviation",All(Shop),tcer=False)],  is_dropdown=True )                           )
    """ store_abbre = CharField()
        niche = CharField()
        page = CharField()
        add_thumbnails = CharField()
        is_free_plus_ship = CharField()
    """
    @staticmethod
    def change_mutaliskconfig_niche():    Update(Muta.objects.all()[0],         niche=  OSA.display_dialog("Pick Your 🔮", dropdown_options=[i.niche for i in keysort("niche",All(Niche),tcer=False)],  is_dropdown=True )                           )
    @staticmethod
    # basically obselete
    def change_mutaliskconfig_page():    Update(Muta.objects.all()[0],         page= OSA.display_dialog("Page 🤒 😌 😗", dropdown_options=[i.name for i in keysort("name",All(Facebookpage),tcer=False)],  is_dropdown=True )                           )
    @staticmethod
    def fudge():
      1
      OSA().notify("FUDGE")
  class New_Menulet:
    def __init__(self):
      """
      You Cannot Use `self` in an eval(exec(`_ _`)), in Dictionaryentry (you made the eval [1] of a list and [0], the setitem(g(),`_ _`,self) ,  then used g()[`_ _`]  )

      """
      import rumps
      import sys
      from rumps import MenuItem as M
      from rumps import MenuItem
      globals().update(locals())
      #self.app = rumps.App("Fig", quit_button=rumps.MenuItem('Quit Fig', key='q'),)
      #self.app = rumps.App("Fig")
      self.app = rumps.App("☃️", quit_button=Null)
      self.set_menu()
      #process(  lambda: [time.sleep(0.3), self.set_menu()]  )
      # [default] process(lambda:([tryprocess(lambda:  ([  setattr(g,"Z",pyperclip.paste().strip())  ,    ,  pyperclip.copy("\n")  ,  ]))       if((Muta()().job_search_on)and(pyperclip.paste().startswith("job: ")))else(zz(0.25))for i in(range(WHILE_TRUE))] ))
      # process(lambda:([tryprocess(lambda:  ([  setattr(g,"Z",pyperclip.paste().strip())  ,  process(lambda:Application2().run(g.Z.split(": ",1)[1].strip()))  ,  pyperclip.copy("\n")  ,  ]))       if((Muta()().job_search_on)and(pyperclip.paste().startswith("job: ")))else(zz(0.25))for i in(range(WHILE_TRUE))] ))
      # process(lambda:([tryprocess(lambda:  ([  setattr(g,"Z",pyperclip.paste().strip())  ,  swamp([lambda:(New_Email().verify()),lambda:ProductTalk().take_it(),lambda:New_Email().take_response(Filter(New_Email,responded=0)[0])], [lambda:g.Z.startswith("support: verify: "), lambda:g.Z.startswith("support: ptalk: "), lambda:g.Z.startswith("support: next: ")])  ,  pyperclip.copy("\n")  ,  Update(Muta()(),new_menulet_changed=1)  ]))       if((Muta()().support_on)and(pyperclip.paste().startswith("support: ")))else(zz(0.25))for i in(range(WHILE_TRUE))] ))
      # process(lambda:([tryprocess(lambda: [ScienceVessel().add() if (pyperclip.paste().startswith("twirl1: ") and Muta()().sciencevessels_on) else sp(0.25)]) for i in range(WHILE_TRUE)]))
      # process(lambda: [Settlement.settlement_depositionz(date=(Date()-1).dateobj), self.set_menu()])
      # process(lambda:[tryprocess(lambda:([setattr(g,"Z",pyperclip.paste().strip()),pyperclip.copy("\n"),pool(lambda:tp(lambda:Product().add_product(),ep=1))] if((Muta()().fig_on)and(pyperclip.paste().startswith("twirl1: ")))else(zz(0.25))))  for i in(range(WHILE_TRUE))] )
      # process(lambda:[tryprocess(lambda:([AddProduct().add() if (pyperclip.paste().startswith("twirl1: ") and Muta()().addproducts_on) else sp(0.25)])) for i in range(WHILE_TRUE)])
      # process(lambda:[tryprocess(lambda:([setattr(g,"Z",pyperclip.paste().strip()),pyperclip.copy("\n"),pool(lambda:tp(lambda:InceptedProduct().X(),ep=1))] if((Muta()().incept_product_on)and(pyperclip.paste().startswith("incept: ")))else(zz(1))))  for i in(range(WHILE_TRUE))] )
      process(lambda:[(swamp([
                                lambda:tryprocess(lambda:[setattr(g,"Z",pyperclip.paste().strip()),pyperclip.copy("\n"),pool(lambda:tp(lambda:Product().add_product(),ep=1))]),
                                lambda:tryprocess(lambda:AddProduct().add()),
                                lambda:tryprocess(lambda:[setattr(g,"Z",pyperclip.paste().strip()),pyperclip.copy("\n"),pool(lambda:tp(lambda:InceptedProduct().X(),ep=1))]),
                                lambda:tryprocess(lambda:ProductChange().add()),
                                lambda:tryprocess(lambda:OSA().notify("start updates")),
                              ],
                              [
                                lambda:((Muta()().fig_on)and(pyperclip.paste().startswith("twirl1: "))),
                                lambda:(pyperclip.paste().startswith("twirl1: ") and Muta()().addproducts_on),
                                lambda:((Muta()().incept_product_on)and(pyperclip.paste().startswith("incept: "))),
                                lambda:(pyperclip.paste().startswith("productchange: ") and Muta()().productchange_on),
                                lambda:(False),
                              ]),sp(0.25)) for i in range(WHILE_TRUE)])
      # process(lambda:[tryprocess(lambda:([ProductChange().add() if (pyperclip.paste().startswith("productchange: ") and Muta()().productchange_on) else sp(0.25)])) for i in range(WHILE_TRUE)])
      # process(lambda:[tryprocess(lambda:([pool(lambda:tp(lambda:Facebookpage().create_facebook_post(Muta()().page),ep=1))] if((pyperclip.paste().startswith("fb_post: ")))else(zz(1))))  for i in(range(WHILE_TRUE))] )

      # process(lambda:[tryprocess(lambda:([setattr(g,"Z",pyperclip.paste().strip()),OSA.log(str(alitracker(*g.Z.split("alitracker: ")[1].split(", ")))),pyperclip.copy("\n"),sp(2)] if(pyperclip.paste().startswith("alitracker: "))else(zz(5))))  for i in(range(WHILE_TRUE))] )
      # process(lambda:[tryprocess(lambda:([setattr(g,"Z",pyperclip.paste().strip()),OSA.log(reverse_image_search(g.Z.split("imagesearch: ")[1])),pyperclip.copy("\n"),sp(2)] if(pyperclip.paste().startswith("imagesearch: "))else(zz(3))))  for i in(range(WHILE_TRUE))] )
      # process(lambda:[tryprocess(lambda:([setattr(g,"Z",pyperclip.paste().strip()),OSA.log(get_ali_url(g.Z.split("get_ali_url: ")[1].split("/")[-1])),pyperclip.copy("\n"),sp(2)] if(pyperclip.paste().startswith("get_ali_url: "))else(sp(2))))  for i in(range(WHILE_TRUE))] )

      # 'process(lambda:(sp(0),[tryprocess(lambda:Updates().update("GhostProductUpdate")) for i in range(WHILE_TRUE)]))\nprocess(lambda:(sp(0),[tryprocess(lambda:Updates().update("ProductsFeed")) for i in range(WHILE_TRUE)]))\nprocess(lambda:(sp(0),[tryprocess(lambda:Updates().update("LineitemsFeed")) for i in range(WHILE_TRUE)]))\nprocess(lambda:(sp(0),[tryprocess(lambda:Updates().update("AdsetUpdates")) for i in range(WHILE_TRUE)])) # FB\nprocess(lambda:(sp(0),[tryprocess(lambda:Updates().update("LineitemUpdates")) for i in range(WHILE_TRUE)])) # ALI, SHOPIFY\nprocess(lambda:(sp(0),[tryprocess(lambda:Updates().update("Aliexpressorder_update")) for i in range(WHILE_TRUE)]))\nprocess(lambda:(sp(0),[tryprocess(lambda:Updates().update("ProductUpdates")) for i in range(WHILE_TRUE)]))\nprocess(lambda:(sp(0),[tryprocess(lambda:Updates().update("New_EmailUpdates")) for i in range(WHILE_TRUE)])) # GMAIL\nprocess(lambda:(sp(0),[tryprocess(lambda:Updates().update("Aliexpressorder_event_update")) for i in range(WHILE_TRUE)]))'
      # process(lambda:(sp(0),[tryprocess(lambda:Updates().update("GhostProductUpdate")) for i in range(WHILE_TRUE)]))
      # process(lambda:(sp(1800),[tryprocess(lambda:Updates().update("ProductsFeed")) for i in range(WHILE_TRUE)]))
      # process(lambda:(sp(900),[tryprocess(lambda:Updates().update("LineitemsFeed")) for i in range(WHILE_TRUE)]))
      # process(lambda:(sp(0),[tryprocess(lambda:Updates().update("AdsetUpdates")) for i in range(WHILE_TRUE)])) # FB
      # process(lambda:(sp(1800),[tryprocess(lambda:Updates().update("LineitemUpdates")) for i in range(WHILE_TRUE)])) # ALI, SHOPIFY
      # process(lambda:(sp(1800),[tryprocess(lambda:Updates().update("Aliexpressorder_update")) for i in range(WHILE_TRUE)]))
      # process(lambda:(sp(1800),[tryprocess(lambda:Updates().update("ProductUpdates")) for i in range(WHILE_TRUE)]))
      # process(lambda:(sp(0),[tryprocess(lambda:Updates().update("New_EmailUpdates")) for i in range(WHILE_TRUE)])) # GMAIL
      # process(lambda:(sp(1800),[tryprocess(lambda:Updates().update("Aliexpressorder_event_update")) for i in range(WHILE_TRUE)]))

      self.app.run()
    @staticmethod
    def plus(callback=lambda: print(1), self=None):
      from rumps import MenuItem
      assert None!=getattr(self,"set_menu")
      return [MenuItem("+",callback=lambda _=None:[(callback)(),self.set_menu()] )]
    def set_menu(self):
      keys = list(self.app.menu.keys())
      redprint(keys)
      for i in keys:
        self.app.menu.pop(i)

      self.app.menu = [

                        # [gl(keysort("created_at",([i for i in All(Product) if i.title not in lmap(lambda i: i.x.split("twirl1: ")[1].split("|")[0],All(ScienceVessel))]+list(All(ScienceVessel))) ),"x"),[M("Created Times"),[M("Refresh",callback=lambda _=None:self.set_menu())]+["%s %s, %s"%("1. ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), Date().seconds_to_text((Date().Now()-gx("x")[0].created_at).total_seconds(),seconds=0) )]+["%s %s, %s"%(("%s. "%(idx+2)),i.created_at,or_list(lambda:Date().seconds_to_text((i.created_at-gx("x")[idx+1].created_at).total_seconds(),seconds=0),"/") ) for idx, i in enum(gx("x"))]]][1],
                        [M(("Setup: |%s|%s|%s|"%(Muta()().store_abbre.upper()if(Muta()().store_abbre)else("-"), (Muta()().niche)if(Muta()().niche)else("-"), (Muta()().page)if(Muta()().page)else("-"), ))),[
                          [MenuItem("Store Abbreviation"),
                            [
                              eval("""MenuItem(Get(Shop,shop_abbreviation="%s").shop_abbreviation.upper(), callback=lambda _=None:[ Update(Muta()(),store_abbre=Get(Shop,shop_abbreviation="%s").shop_abbreviation), self.set_menu()] )"""%(i.shop_abbreviation,i.shop_abbreviation)) for i in All(Shop)
                            ] + [[setitem(g(),"fig_x",self),MenuItem("-", callback=lambda _=None:[ Update(All(Muta)[0],store_abbre="-"), g()["fig_x"].set_menu()] )][1]]
                          ],
                          [MenuItem("Niche"),
                            [setitem(g(),"fig_x",self),[MenuItem("+", callback=lambda _=None:[tryprocess(Niche(date_added=datetime.now(),niche=OSA.display_dialog("Niche?", [":)"]) ).save),Update(Muta()(),niche=list(All(Niche))[-1].niche),OSA().notify("added niche %s & clearing clipboard [%s]" % (pyperclip.paste(),(len(Filter(Niche,niche=pyperclip.paste())))) ),pyperclip.copy(""),self.set_menu() ]) ]+[
                              eval("""[exec("from rumps import MenuItem",globals()),MenuItem('''%s''' if (datetime.now()-Get(Niche,niche='''%s''').date_added).days>15 else '''%s (NEW)''', callback=lambda _=None:[Update(All(Muta)[0],niche='''%s'''),g()["fig_x"].set_menu() ] )][1]"""%(i,i,i,i)) for i in key("niche",keysort("niche",All(Niche),tcer=False)) if i!=""
                            ]][1] + [[setitem(g(),"fig_x",self),MenuItem("-", callback=lambda _=None:[ Update(All(Muta)[0],niche="-"), g()["fig_x"].set_menu()] )][1]]
                          ],
                          # [MenuItem("Is Free Plus Ship"),
                          #   [
                          #     [setitem(g(),"fig_x",self),MenuItem("True", callback=lambda _=None:[ Update(All(Muta)[0],is_free_plus_ship=True), g()["fig_x"].set_menu()] )][1],
                          #     [setitem(g(),"fig_x",self),MenuItem("False", callback=lambda _=None:[ Update(All(Muta)[0],is_free_plus_ship=False), g()["fig_x"].set_menu()] )][1],
                          #   ]
                          # ],
                          [MenuItem("Page"),
                            [setitem(g(),"fig_x",self),[MenuItem("/",callback=lambda _=None:[get_pages(),self.set_menu()])]+[
                              eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s", callback=lambda _=None:[ Update(All(Muta)[0],page="%s"),g()["fig_x"].set_menu()] )][1]"""%(i,i)) for i in key("name",keysort("name",All(Facebookpage),tcer=False))
                            ]][1] + [[setitem(g(),"fig_x",self),MenuItem("-", callback=lambda _=None:[ Update(All(Muta)[0],page="-"), g()["fig_x"].set_menu()] )][1]]
                          ],
                        ]],
                        # [globalise(self,"new_menulet_x"),[M("Change Shop (Current Shop: %s)"% (Muta()().store_abbre)), [eval("""M("%s",callback = lambda _=None:[Update(Muta()(),store_abbre="%s")])"""%(i.shop_abbreviation,i.shop_abbreviation)) for i in All(Shop)]]][1],
                        # [MenuItem("Active - 1. Subscriptions (Rolling $%s)"%((round((sum(lmap(float,key("price_per_month",All(Subscription)))))/ list(([exec("from calendar import monthrange",globals()),monthrange(datetime.now().year,datetime.now().month)][1]))[1],2)))),
                        #   [
                        #     [M("Today"), M("($%s)"%((round((sum(lmap(float,key("price_per_month",All(Subscription)))))/ list(([exec("from calendar import monthrange",globals()),monthrange(datetime.now().year,datetime.now().month)][1]))[1],2)) ))],
                        #     [M("Subscriptions"), [M("+",callback=lambda _=None:[Save(Subscription,name=OSA.display_dialog("Name?",default_answer=""),price_per_month=float(OSA.display_dialog("price per month?\n(it's okay to round)",default_answer=""))),self.set_menu()])]+[M("%s @ %s"%(i.name,i.price_per_month)) for i in keysort("name",Filter(Subscription,),tcer=False)]+[M("-",callback=lambda _=None:[Del(Get(Subscription,name=OSA.display_dialog("Subscription name?",default_answer=""))),self.set_menu()])]],
                        #     [M("For This Month"), ["%s: ($%s)"%((Date().friendlydate(datetime(datetime.now().year,datetime.now().month,(i+1)),only_date=True)),round(((sum(lmap(float,key("price_per_month",All(Subscription)))))/ list(([exec("from calendar import monthrange",globals()),monthrange(datetime.now().year,datetime.now().month)][1]))[1] ),2)) for i in lrange(datetime.now().day)]]
                        #   ]
                        # ],
                        [M("Main"),
                        [
                        [MenuItem("Active - 7. Routing (%s, (%s, %s), (%s, %s), %s)"%(
                                                                                        len(onyx("e1")),
                                                                                        len([i for i in onyx("e2") if i.calculate_time_so_far()<=20]),
                                                                                        len([i for i in onyx("e2") if i.calculate_time_so_far()>20]),
                                                                                        len([i for i in onyx("e3") if i.calculate_time_so_far()<=20]),
                                                                                        len([i for i in onyx("e3") if i.calculate_time_so_far()>20]),
                                                                                        len(onyx("e4")) )),
                          [sudcall("calculate",onyx_lineitems())if(Muta()().show_routing)else(None),[
                            [M("Showing Routing" if Muta()().show_routing == True else "Routing Off"), [M("Showing Routing" if Muta()().show_routing == True else "Routing Off",callback=lambda _=None:[Update(Muta()(),show_routing=True if Muta()().show_routing == False else False if Muta()().show_routing == True else True),self.set_menu()])]],
                            ["Ready To Order",[[M("%s (%s)"%(i,
                                                len([q for q in Filter(Lineitem,stage="%s"%("e1"),timesofar=(i))])
                                              )
                                  ),
                                  [[M("ID: %s"%(x.id)),eval("""[M("Copy ID %s To Clipboard",callback=lambda _=None:[pyperclip.copy("%s")])]"""%(x.id,x.id))+[eval("""M("%s",callback=lambda _=None:[OSA.log("%s")])"""%(i,i)) for i in or_list(lambda:Get(Lineitem,id=x.id).tracking_events,[])]] for x in Filter(Lineitem,stage="%s"%("e1"),timesofar=(i))]
                                ] for i in lrange(max(sud("timesofar",Filter(Lineitem,stage="e1"))+[0])+(1))]
                            ] if Muta()().show_routing else None,
                            ["Placed Order",[[M("%s (%s)"%(i,
                                                len([q for q in Filter(Lineitem,stage="%s"%("e2"),timesofar=(i))])
                                              )
                                  ),
                                  [[M("ID: %s"%(x.id)),eval("""[M("Copy ID %s To Clipboard",callback=lambda _=None:[pyperclip.copy("%s")])]"""%(x.id,x.id))+[eval("""M("%s",callback=lambda _=None:[OSA.log("%s")])"""%(i,i)) for i in or_list(lambda:Get(Lineitem,id=x.id).tracking_events,[])]] for x in Filter(Lineitem,stage="%s"%("e2"),timesofar=(i))]
                                ] for i in lrange(max(sud("timesofar",Filter(Lineitem,stage="e2"))+[0])+(1))]
                            ] if Muta()().show_routing else None,
                            ["Tracking And Shipping",[[M("%s (%s)"%(i,
                                                len([q for q in Filter(Lineitem,stage="%s"%("e3"),timesofar=(i))])
                                              )
                                  ),
                                  [[M("ID: %s"%(x.id)),eval("""[M("Copy ID %s To Clipboard",callback=lambda _=None:[pyperclip.copy("%s")])]"""%(x.id,x.id))+[eval("""M("%s",callback=lambda _=None:[OSA.log("%s")])"""%(i,i)) for i in or_list(lambda:Get(Lineitem,id=x.id).tracking_events,[])]] for x in Filter(Lineitem,stage="%s"%("e3"),timesofar=(i))]
                                ] for i in lrange(max(sud("timesofar",Filter(Lineitem,stage="e3"))+[0])+(1))]
                            ] if Muta()().show_routing else None,
                            ["Delivered",[[M("%s (%s)"%(i,
                                                len([q for q in Filter(Lineitem,stage="%s"%("e4"),timesofar=(i))])
                                              )
                                  ),
                                  [[M("ID: %s"%(x.id)),eval("""[M("Copy ID %s To Clipboard",callback=lambda _=None:[pyperclip.copy("%s")])]"""%(x.id,x.id))+[eval("""M("%s",callback=lambda _=None:[OSA.log("%s")])"""%(i,i)) for i in or_list(lambda:Get(Lineitem,id=x.id).tracking_events,[])]] for x in Filter(Lineitem,stage="%s"%("e4"),timesofar=(i))]
                                ] for i in lrange(max(sud("timesofar",Filter(Lineitem,stage="e4"))+[0])+(1))]
                            ] if Muta()().show_routing else None,
                          ]][1]
                        ],

                        [globalise(self,"support_x"),[M("Active - 8. Support"),
                          [M("/",callback=lambda _=None:[lmap(lambda i:New_Email().new_email_set(i.shop_abbreviation),All(Shop)),self.set_menu()])]+[[i,
                          [[("%s: (%s) (MATCHED BUYER)"%(a,Join(",",lmap(str,key("order_number",keysort("order_number",Filter(Order,email=a,shop=i),False)))))),
                          [
                          eval("""M((Get(%s,id=%s).printformat()), callback=lambda _=None: [tr(lambda:Get(%s,id=%s).run_support(),ep=1),globe("support_x").set_menu()])"""%(type(b).__name__,b.id,type(b).__name__,b.id)) for b in New_Email().get_all_support_items(email=a,shop=i) ]
                                           ] for a in New_Email().get_all_identified_emails(i)]
                          ] for i in key("shop_abbreviation",All(Shop))]
                        ]][1],
                        
                        # [M("Active - 8. Support"),
                        #   [[i,[[("%s: (%s) (MATCHED BUYER)"%(a,Join(", ",lmap(str,key("order_number",keysort("order_number",Filter(Order,email=a,shop=i),False)))))),[M("%s: %s"%(Date().friendlydate(b.date,with_year=True), (b.true_id)if(type(b)==New_Email)else(b.invoice_id)),callback=lambda _=None:[(b.run_support())if(type(b)==New_Email)else(b.run_support()),self.set_menu()]) for b in sorted(list(Filter(New_Email,emailer=a,shop=i))+list(Filter(TertiaryAction,email=a,shop=i)),key=lambda i:(i.date)if(type(i)==New_Email)else(i.date)) ]] for a in New_Email().get_identified_emails(i)]] for i in key("shop_abbreviation",All(Shop))]
                        #   #[[i,[[("%s: (%s) (MATCHED BUYER)"%(a,Join(", ",lmap(str,key("order_number",keysort("order_number",Filter(Order,email=a,shop=i),False)))))),[eval("""M("%s: %s %s",callback=lambda _=None:[((or_list(lambda:Get(New_Email,true_id="%s"),lambda:Get(TertiaryAction,invoice_id="%s"))).run_support())if(type((or_list(lambda:Get(New_Email,true_id="%s"),lambda:Get(TertiaryAction,invoice_id="%s"))))==New_Email)else((or_list(lambda:Get(New_Email,true_id="%s"),lambda:Get(TertiaryAction,invoice_id="%s"))).run_support()),self.set_menu()])"""%(Date().friendlydate(b.date,with_year=True), (b.true_id)if(type(b)==New_Email)else(b.invoice_id), ("(Tagged With Order Numbers %s)" %(", ".join(lmap(str,sorted(b.tagged_order_numbers)))))if(type(b)==New_Email and b.tagged_order_numbers)else("Not Tagged With Any Order Numbers")if(type(b)==New_Email and b.tagged_order_numbers==None)else(("(Order Number %s)"%(Get(Order,id=b.order_id).order_number))), ((b.true_id)if(type(b)==New_Email)else(b.invoice_id)),((b.true_id)if(type(b)==New_Email)else(b.invoice_id)),((b.true_id)if(type(b)==New_Email)else(b.invoice_id)),((b.true_id)if(type(b)==New_Email)else(b.invoice_id)),((b.true_id)if(type(b)==New_Email)else(b.invoice_id)),((b.true_id)if(type(b)==New_Email)else(b.invoice_id)),)) for b in sorted(list(Filter(New_Email,emailer=a,shop=i))+list(Filter(TertiaryAction,email=a,shop=i)),key=lambda i:(i.date)if(type(i)==New_Email)else(i.date)) ]] for a in New_Email().get_identified_emails(i)]] for i in key("shop_abbreviation",All(Shop))]
                        # ],
                        
                        # [globalise(self,"new_menulet_x"),[MenuItem("Active - 8. New_Email (%s To Read)"%(len(Filter(New_Email,responded=0)))),
                        #   [
                        #     #[M("%s"%(i)), [[i, [ eval("""M("🌭",callback=lambda _=None:[New_Email().take_response(Get(New_Email,id=%s)),globe("new_menulet_x").set_menu()])"""%i.id) for i in Filter(New_Email,emailer=i,responded=0)]] for i in sorted(set(key("emailer",Filter(New_Email,email=i,responded=0))))]] for i in sorted(key("Business_Email_Address",All(Shop)))
                        #     #[M("%s"%(i)), [eval("""[M("Update emails for %s"),M("Update emails for %s",callback=lambda _=None:[New_Email().new_email_set("%s"),globe("new_menulet_x").set_menu()])]"""%(i,i,i))]+[[i, [ eval("""M("🍭",callback=lambda _=None:[New_Email().take_response(Get(New_Email,id=%s)),globe("new_menulet_x").set_menu()])"""%i.id) for i in Filter(New_Email,emailer=i,responded=0)]] for i in sorted(set(key("emailer",Filter(New_Email,email=i,responded=0))))]] for i in sorted(key("Business_Email_Address",All(Shop)))
                        #     [M("%s"%(i)), [eval("""[M("Update emails for %s"),M("Update emails for %s",callback=lambda _=None:[New_Email().new_email_set("%s"),globe("new_menulet_x").set_menu()])]"""%(i,i,i))]+[[M("Completed"),[eval("""[M("❄️"),[Get(New_Email,id=%s).emailer]]"""%(i.id)) for i in Filter(New_Email,email=i,responded=1)]]]+[[i, [ eval("""M("🍭",callback=lambda _=None:[New_Email().take_response(Get(New_Email,id=%s)),globe("new_menulet_x").set_menu()])"""%i.id) for i in Filter(New_Email,emailer=i,responded=0)]] for i in sorted(set(key("emailer",Filter(New_Email,email=i,responded=0))))]] for i in sorted(key("Business_Email_Address",All(Shop)))
                        #   ]
                        # ]][1],

                        [globalise(self,"product_talk_x"),[MenuItem("Active - 9. Product Talk (%s, %s)"%(len(lset(key("id",All(ProductTalk)))),len(Filter(ProductTalk,shop=Muta()().store_abbre)))),
                          [M("+",callback=lambda _=None:[ProductTalk().create_2(),self.set_menu()])]+[
                            [
                              M(Get(Product,id=i.product_id).title),[
                                                                        [
                                                                          i.supplier,
                                                                                    [
                                                                                        Get(Product,id=c.product_id).title for c in Filter(ProductTalk,supplier=i.supplier)
                                                                                    ]
                                                                                    
                                                                        ] 
                                                                      ]
                                                                    ] for i in tcer(sorted(Filter(ProductTalk,shop=Muta()().store_abbre),key=lambda i:len(Filter(Lineitem,id=i.product_id))))
                            ]+[M("-",callback=lambda _=None:[ProductTalk().delete(OSA.log("Title?")),self.set_menu()])]
                        ]][1],


                        [M("Active - 10. Product Inceptions"),
                          [[M("Showing" if Muta()().show_product_inceptions == True else "Not Showing"),M("Showing" if Muta()().show_product_inceptions == True else "Not Showing",callback=lambda _=None:[Update(Muta()(),show_product_inceptions = True if Muta()().show_product_inceptions == False else False if Muta()().show_product_inceptions == True else True),self.set_menu()])]]+
                          [
                            #i.title,((Date().Now())-(i.last_check)).days,i.id
                            #[M(i),[ eval("""M("%s (%s Days Unavailable)",callback=lambda _=None:[r_image_search(pool(Images().download,key("src",Get(Product,id=%s).images)).result(),True)])"""%(i.title,((Date().Now())-(i.last_check)).days,i.id )) for i in Product().is_availables(shop=i)]] for i in key("shop_abbreviation",All(Shop))]
                            [M(i),[
                                [M("%s (%s Days Unavailable, %s Running Adsets With This Product, %s Pending Orders With This Product)"%(i.title,
                                      ((Date().Now())-(i.last_check)).days,
                                      len(Filter(Adset,shop_abbreviation=i.shop,handle=i.handle,status="ACTIVE")),
                                      len(set(key("order_id",[x for x in onyx_lineitems("e1") if x.product_id==i.id])))
                                      )
                                  ), 
                                  eval("""[M("Find Products Like These",callback=lambda _=None:[
                                            r_image_search(pool(Images().download,key("src",Get(Product,id=%s).images)).result(),True)] ),[
                                            M("Running Adsets With This Product ({})".format( len(Filter(Adset,shop_abbreviation="%s",handle="%s"))) ),
                                            [M("Adset ID: {}".format(i.id)) for i in Filter(Adset,shop_abbreviation="%s",handle="%s")]]]"""%(i.id,i.shop,i.handle,i.shop,i.handle))
                                ] for i in Product().is_unavailables(shop=i)]] if Muta()().show_product_inceptions else None for i in key("shop_abbreviation",All(Shop))
                            ]
                          ],
                        #@confirmed to reset menu
                        #[MenuItem("Active - 7. CruxSupplier (Parked (Until Any CruxSupplier))"),
                        ##  [MenuItem("A"),MenuItem("B")]
                        #],
                        #[MenuItem("Active - 4. CruxSupplier"),
                        #  [MenuItem("Why Does This Work?",callback=lambda _=None:OSA.display_dialog(default_answer="Sure u look it up, look up GhostProduct u can destroy Product|technically from a event of now, i do not have any CruxSuppliers., technically from a event of now, i do not have any CruxSuppliers.\n\nKeep In Mind, If There This is a cruxsupplier... It will possess cruxsupplier orders/existing orders/bad orders\n\nAt This Moment, I am still looking for the first CruxSupplier"))]+[
                        #    [MenuItem(i.vendor),[[MenuItem("removable products"),[eval("MenuItem('productId:%s, vendor:%s (Logged As CruxSupplier)', callback=lambda _=None:[Shop()('%s').pfind(id_='%s').destroy() if eval(OSA.display_dialog('rly destroy? evaluating... (0/1)'))==1 else None,OSA.notify('%s destroyed == %s')] )"%(x.id,(x.aliexpressvendor if x.aliexpressvendor else x.amazonvendor),x.shop,x.id,x.id,("False, could Find" if 1== tryprocess(Shop()(x.shop).pfind,id_=x.id) else "True, could Not Find") )) for x in All(Product) if (x.aliexpressvendor == i.vendor or x.amazonvendor == i.vendor)]],[MenuItem("cruxsupplier orders (a list to get a quantity of how many lineitems are with this CruxSupplier's Products)"),[eval("MenuItem(%s, callback = lambda _=None:OSA.notify('%s|%s') )"%(x.id, x.id,x.id)) for x in  [x for x in onyx_lineitems() if Get(GhostProduct,id=x.product_id).aliexpressvendor == i.vendor or Get(GhostProduct,id=x.product_id).amazonvendor == i.vendor ] ]], ]] for i in All(CruxSupplier)
                        #  ]
                        #],
                        [M("Active - 11. Order Unpender"),
                          [
                            M("Order Unpender",callback = lambda _=None:[os.system("cd ~/tavern/tavern && ~/tavern/bin/python3.5 -c 'from soda.can import *; Order_Unpender()()' &")])
                          ]
                        ],
                        ]
                        ],

                        [MenuItem("Transactions"),
                        [
                        [globalise(self,"new_menulet_x"),[MenuItem("Active - 2. AceInTheHole (%s Days Behind, %s Untagged, latest date: %s)"%( or_list(lambda:((Date()-1)-(Date(max([max(key("date",All(AceInTheHole))),list(All(AceInTheHole))[-1].date])))),"X"), or_list(lambda:len(Filter(AceInTheHole,tag=None)),"X"),or_list(lambda:Date(max(sud("date",All(AceInTheHole)))),lambda:"X") )),
                          [
                            M("+ (%s)"%("headers: date, description, amount"),callback=lambda _=None:[AceInTheHole().accept_csv(get_latest_download()),self.set_menu()]),
                            [M("Shop for headers: %s, Account for headers: %s" % (Muta()().store_abbre, or_list(lambda:Get(AceInTheHoleHeaderColumns,shop=Muta()().store_abbre,account=Muta()().Active_AceInTheHole_header_column_account_name).account,lambda:"None Selected") )),
                             [M("+",callback=lambda _=None:[AceInTheHoleHeaderColumns().add(),self.set_menu()])]+\
                             [eval("""M("%s - %s",callback=lambda _=None:[Update(Muta()(),Active_AceInTheHole_header_column_account_name="%s"),globals()["new_menulet_x"].set_menu()])"""%(i.account,str(list(i.header_column_dict.items())).replace("'","").replace(","," for"),i.account)) for i in Filter(AceInTheHoleHeaderColumns,shop=Muta()().store_abbre)]
                             ],
                            [M("Types (Add Tags, %s Tags)"%(len(All(AceInTheHoleTypeTag)))),
                              [M("+",callback=lambda _=():[lmap(lambda i:Save(AceInTheHoleType,name=i.strip()),OSA.display_dialog("Type(s) [note: many can be added by separating them with a comma]?",default_answer="").split(",")),globe("new_menulet_x").set_menu()])]+[eval("""[M("%s"),[M("+",lambda _=None:[lmap(lambda i: Save(AceInTheHoleTypeTag,tag=i.strip(),type="%s",sign=OSA.display_dialog("Will this amount for the tag “{}” be positive, negative, or does it not apply to this tag?".format(i.strip()),dropdown_options=["positive","negative","positive_or_negative"])),OSA.display_dialog("Tag?",default_answer="").split(",") ),globe("new_menulet_x").set_menu()])]+[eval('''[M('{}'),M('Run',callback=lambda _=None:[[(AceInTheHoleTypeTag().run_tag(type="{}",tag="{}")),globe("new_menulet_x").set_menu()]if(OSA.display_dialog("This will run all for {}, {}, continue?",text_prompt=False,buttons=["NO","OK"])=="OK")else()])]'''.format(i.tag,i.type,i.tag,i.type,i.tag),globals()) for i in keysort("tag",Filter(AceInTheHoleTypeTag,type="%s"),tcer=False)]          +[M("-",callback=lambda _=None:[Del(Get(AceInTheHoleTypeTag,type="%s",tag=OSA.display_dialog("Tag to delete?",default_answer=""))),globe("new_menulet_x").set_menu() ])]]"""%(i.name,i.name,i.name,i.name),globals()) for i in keysort("name",All(AceInTheHoleType),tcer=False)]+[M("Run All Tags",callback=lambda _=None:[AceInTheHoleTypeTag().run_all(),self.set_menu()])]+[M("-",callback=lambda _=():[Del(Get(AceInTheHoleType,name=OSA.display_dialog("Type to delete?",default_answer=""))),globe("new_menulet_x").set_menu()])]
                            ],
                            [M("View Current Untagged (%s Untagged)"%(len(Filter(AceInTheHole,tag=None,type=None)))), [eval("""M("%s")"""%(i.amount)) for i in Filter(AceInTheHole,tag=None,type=None)]],
                            [M("View Current Untagged Transaction Details (View Now)"),M("View Current Untagged Transaction Details",callback=lambda _=None:[[OSA.display_dialog(q="Columns: account, date, amount, type, tag, description, shop\nYou can paste this into Excel",buttons=[" "*250+"OK"+" "*250],default_answer=("\n".join(["%s\t%s\t%s\t%s\t%s\t%s\t%s\t"%(i.account,i.date,i.amount,i.type,i.tag,i.description[:100],i.shop) for i in Filter(AceInTheHole,tag=None,type=None)])))],self.set_menu()])],
                            [M("View Current Tagged Transactions (%s)"%(len(Filter(AceInTheHole,~Q(tag=None),shop=Muta()().store_abbre)))),M("View Current Tagged Transaction",callback=lambda _=None:[[OSA.display_dialog(q="Columns: account, date, amount, type, tag, description, shop\nYou can paste this into Excel",buttons=[" "*250+"OK"+" "*250],default_answer=("\n".join(["%s\t%s\t%s\t%s\t%s\t%s\t%s\t"%(i.account,i.date,i.amount,i.type,i.tag,i.description[:100],i.shop) for i in Filter(AceInTheHole,~Q(tag=None),~Q(type=None),shop=Muta()().store_abbre)])))],self.set_menu()])],
                          ]
                        ]][1],
                        [globalise(self,"new_menulet_x"),[MenuItem("Active - 3. Approved Transactions (%s Days Behind For Tagged, %s To Approve)"% ( or_list(lambda:(((Date(max([max(key("date",Filter(AceInTheHole,shop=Muta()().store_abbre))),list(Filter(AceInTheHole,shop=Muta()().store_abbre))[-1].date])))) - ((Date(max([max(key("date",Filter(ApprovedTransaction,shop=Muta()().store_abbre))),list(Filter(ApprovedTransaction,shop=Muta()().store_abbre))[-1].date]))))),"X") , or_list(lambda:len(Filter(ApprovedTransaction,approved=0,shop=Muta()().store_abbre)),"X") )),
                          [
                            [M("Load Approved Transactions"), M("Load Approved Transactions",callback=lambda _=None:[[Save(ApprovedTransaction,account=i.account,date=i.date,price=i.amount,type=i.type,tag=i.tag,description=i.description,id=i.id,approved=0,shop=i.shop) for i in Filter(AceInTheHole,~Q(type=None),~Q(tag=None),shop=Muta()().store_abbre) if i.id not in key("id",Filter(ApprovedTransaction,shop=Muta()().store_abbre))],globe("new_menulet_x").set_menu()] if(len([i for i in Filter(AceInTheHole,~Q(type=None),~Q(tag=None),shop=Muta()().store_abbre) if i.id not in key("id",Filter(ApprovedTransaction,shop=Muta()().store_abbre))])!=0)else(OSA.display_dialog("Already Loaded All Transactions.\nType OK to continue",default_answer="")))],
                            [M("To Approve (%s)"%(len(Filter(ApprovedTransaction,approved=0)))), [eval("""M("%s",callback=(lambda _=None:[(Update(Get(ApprovedTransaction,id=%s),approved=1,what_i_think_my_current_balance_is=OSA.display_dialog("What do you think your current balance is?",default_answer="")))if(OSA.display_dialog("PLEASE READ\\n************************************\\nThis is your current balance: {}\\nType I APPROVE to begin the approval process for this charge\\nIn %s at %s of $%s with type %s and tag %s and description: %s\\n************************************".format((or_list(tryreturn(lambda:Filter(ApprovedTransaction,approved=1).n(-1).what_i_think_my_current_balance_is),"N/A") )),default_answer="",buttons=[" "*140+"OK"+" "*140])=="I APPROVE")else(),globe("new_menulet_x").set_menu()])if(%s==0)else(None) )"""%(i.price,i.id,i.account,Date().friendlydate(i.date,only_date=True),i.price,i.type,i.tag,i.description,idx)) for idx,i in enum( Filter(ApprovedTransaction,approved=False) )]],
                            [M("What I Think My Current Balance Is"),M("What I Think My Current Balance Is: $%s"%(or_list(tryreturn(lambda:Filter(ApprovedTransaction,approved=1,shop=Muta()().store_abbre).n(-1).what_i_think_my_current_balance_is),"N/A")))],
                            [M("What I Think My Current Balance Is - All"), [M("$%s"%i.what_i_think_my_current_balance_is) for i in tcer(Filter(ApprovedTransaction,approved=1,shop=Muta()().store_abbre))]]
                          ]
                        ]][1],
                        [MenuItem("Active - 4. Settlements /When/ (%s Days Behind)"%( or_list(lambda:((Date()-1)-(Date(max([max(key("date",Filter(Settlement,shop=Muta()().store_abbre))),list(Filter(Settlement,shop=Muta()().store_abbre))[-1].date])))),"X") )),
                          [M("+",callback=lambda _=None:[globalise(Date(OSA.log("Date [in format: YYYY-MM-DD]?"))(),"settlement_run_date"),globalise(OSA.log("Running a settlement for the current day will create a settlement with the results of the day up until the run time. This settlement date will have to be run again the next date to update all data for this day to be the most current. Click Exit to exit or click OK to continue.",tp=False,buttons=["Exit","OK"]),"settlement_run_date_today")if(globe("settlement_run_date")==(Date()))else(),((0/0))if(globe("settlement_run_date_today")=="Exit")else(),Settlement()(globe("settlement_run_date")),self.set_menu()])]+[
                            [M("%s"%(Date().friendlydate(i.date,only_date=1))),[
                            M("(sales) (%s)"%(i.sales)),
                            M("(ads) (%s)"%(i.ads)),
                            M("(cogs) (%s)"%(i.cogs)),
                            M("(secondaryaction) (%s)"%(i.refunds)),
                            M("(tertiaryaction) (%s)"%(i.chargebacks)),
                            M("(prdcts added) (%s)"%(i.products_added)),
                            M("(ads added) (%s)"%(i.adsets_added)),
                            M("(rake) (%s)"%(i.rake)),
                            ]] for i in tcer(keysort("date",Filter(Settlement,shop=Muta()().store_abbre)))
                          ]
                        ],
                        # [M("Active - 5. Updates"),
                        #   [
                        #     # M("Aliexpressorder_event_update - Ready To Run",callback=lambda x:[setattr(x,"title","Check for Aliexpressorder_event - Running"),globalise(pool(lambda:Updater().Aliexpressorder_event_update()),"updater_aliexpressorder_event_update"),process(lambda:[setattr(x,"title","Aliexpressorder_event_update - Finished Running, Ready To Run") for i in range(WHILE_TRUE) if globe("updater_aliexpressorder_event_update").is_running() == False])]),
                        #     M("Update_TertiaryActions - Ready To Run (headers: invoice_id, date, requires_response_by, status, order_problem, email, dispute_amount)",callback=lambda x:[setattr(x,"title","Update TertiaryActions - Running"),globalise(pool(lambda:Updater().Update_TertiaryActions()),"updater_update_tertiaryactions"),process(lambda:[setattr(x,"title","Update_TertiaryActions - Finished Running, Ready To Run") for i in range(WHILE_TRUE) if globe("updater_update_tertiaryactions").is_running() == False])]),
                        #     M("Update_Payments - Ready To Run (headers: id, created_at, amount, email, invoice_id, order_id, payment_gateway_name, shop)",callback=lambda x:[setattr(x,"title","Update Payments - Running"),globalise(pool(lambda:Updater().Update_Payments()),"updater_update_payments"),process(lambda:[setattr(x,"title","Update_Payments - Finished Running, Ready To Run") for i in range(WHILE_TRUE) if globe("updater_update_payments").is_running() == False])]),
                        #     M("Update_Payouts - Ready To Run (headers: id, created_at, amount, account_name, account_last_4_digits, payment_gateway_name, shop)",callback=lambda x:[setattr(x,"title","Update Payouts - Running"),globalise(pool(lambda:Updater().Update_Payouts()),"updater_update_payouts"),process(lambda:[setattr(x,"title","Update_Payouts - Finished Running, Ready To Run") for i in range(WHILE_TRUE) if globe("updater_update_payouts").is_running() == False])]),

                        #   ]
                        # ],
                        [MenuItem("Active - 6. Updates"),
                          [globalise(TransactionVerification().get_excess_transaction_verification_data(),"transactionverification_y"),[
                            [M("Lineitem Order IDS to Ali Order IDS"), [
                                    [M("Excess Lineitem AliExpress Order IDS to AliExpress Order IDS (%s%% %s matched) (Unknown)"%(globe("transactionverification_y")[10],len(globe("transactionverification_y")[0]))), TransactionVerification().verify_no_excess_aliexpress_orders()],
                                    [M("Excess AliExpress Order IDS to Lineitem AliExpress Order IDS (%s%% %s matched) (Unknown)"%(globe("transactionverification_y")[11],len(globe("transactionverification_y")[1]))), TransactionVerification().verify_no_excess_saved_aliexpress_order_ids()],
                                    ]],
                            [M("Lineitem AliExpress Order Pay Price Amounts to Bank Account Price Amounts"), [
                                    [M("Excess Lineitem AliExpress Price Amounts to Bank Account AliExpress Payment Price Amounts (%s%% %s matched) (Unknown)"%(globe("transactionverification_y")[12],len(globe("transactionverification_y")[2]))), TransactionVerification().verify_no_excess_aliexpress_card_transactions()],
                                    [M("Excess Bank Account AliExpress Payment Price Amounts to Lineitem AliExpress Price Amounts (%s%% %s matched) (Unknown)"%(globe("transactionverification_y")[13],len(globe("transactionverification_y")[3]))), TransactionVerification().verify_no_excess_saved_ordered_aliexpress_order_transactions()],
                                    ]],
                            [M("Order Paid Price Amounts to Gateway Payment Price Amounts *Impacted"), [
                                    [M("Excess Order Prices Amounts to Payment Gateway Sale Order Price Amounts (%s%% %s matched) (Unknown)"%(globe("transactionverification_y")[14],len(globe("transactionverification_y")[4]))), TransactionVerification().verify_no_excess_order_price_amounts_to_payment_gateway_sale_order_price_amounts()],
                                    [M("Excess Payment Gateway Sale Order Price Amounts to Order Prices Amounts (%s%% %s matched) (Unknown)"%(globe("transactionverification_y")[15],len(globe("transactionverification_y")[5]))), TransactionVerification().verify_no_excess_payment_gateway_sale_order_price_amounts_to_order_price_amounts()],
                                    ]],
                            [M("Bank Account Deposits to Payment Gateway Payouts"), [
                                    [M("Excess Bank Account Payment Gateway Deposits to Payment Gateway Payouts To Bank Account (%s%% %s matched) (Unknown)"%(globe("transactionverification_y")[16],len(globe("transactionverification_y")[6]))), TransactionVerification().verify_no_excess_bank_account_payment_gateway_deposits_to_payment_gateway_payouts_to_bank_account()],
                                    [M("Excess Payment Gateway Payouts To Bank Account to Bank Account Payment Gateway Deposits (%s%% %s matched) (Unknown)"%(globe("transactionverification_y")[17],len(globe("transactionverification_y")[7]))), TransactionVerification().verify_no_excess_payment_gateway_payouts_to_bank_account_to_bank_account_payment_gateway_deposits()],
                                    ]],
                            [M("Adspend charges to saved adspend charges"), [
                                    [M("Excess adspend charges to saved adspend charges (%s%% %s matched) (Unknown)"%(globe("transactionverification_y")[18],len(globe("transactionverification_y")[8]))), TransactionVerification().verify_no_excess_adspend_charges()],
                                    [M("Excess saved adspend charges to adspend charges (%s%% %s matched) (Unknown)"%(globe("transactionverification_y")[19],len(globe("transactionverification_y")[9]))), TransactionVerification().verify_no_excess_card_transaction_adspend_charges()],
                                    ]],

                            # [M("Lineitem Order IDS to Ali Order IDS"), [
                            #         [M("Excess Lineitem AliExpress Order IDS to AliExpress Order IDS (Unknown)"), TransactionVerification().verify_no_excess_aliexpress_orders()],
                            #         [M("Excess AliExpress Order IDS to Lineitem AliExpress Order IDS (Unknown)"), TransactionVerification().verify_no_excess_saved_aliexpress_order_ids()],
                            #         ]],
                            # [M("Lineitem AliExpress Order Pay Price Amounts to Bank Account Price Amounts"), [
                            #         [M("Excess Lineitem AliExpress Price Amounts to Bank Account AliExpress Payment Price Amounts (Unknown)"), TransactionVerification().verify_no_excess_aliexpress_card_transactions()],
                            #         [M("Excess Bank Account AliExpress Payment Price Amounts to Lineitem AliExpress Price Amounts (Unknown)"), TransactionVerification().verify_no_excess_saved_ordered_aliexpress_order_transactions()],
                            #         ]],
                            # [M("Order Paid Price Amounts to Gateway Payment Price Amounts *Impacted"), [
                            #         [M("Excess Order Prices Amounts to Payment Gateway Sale Order Price Amounts (Unknown)"), TransactionVerification().verify_no_excess_order_price_amounts_to_payment_gateway_sale_order_price_amounts()],
                            #         [M("Excess Payment Gateway Sale Order Price Amounts to Order Prices Amounts (Unknown)"), TransactionVerification().verify_no_excess_payment_gateway_sale_order_price_amounts_to_order_price_amounts()],
                            #         ]],
                            # [M("Bank Account Deposits to Payment Gateway Payouts"), [
                            #         [M("Excess Bank Account Payment Gateway Deposits to Payment Gateway Payouts To Bank Account (Unknown)"), TransactionVerification().verify_no_excess_bank_account_payment_gateway_deposits_to_payment_gateway_payouts_to_bank_account()],
                            #         [M("Excess Payment Gateway Payouts To Bank Account to Bank Account Payment Gateway Deposits (Unknown)"), TransactionVerification().verify_no_excess_payment_gateway_payouts_to_bank_account_to_bank_account_payment_gateway_deposits()],
                            #         ]],
                            # [M("Adspend charges to saved adspend charges"), [
                            #         [M("Excess adspend charges to saved adspend charges (Unknown)"), TransactionVerification().verify_no_excess_adspend_charges()],
                            #         [M("Excess saved adspend charges to adspend charges (Unknown)"), TransactionVerification().verify_no_excess_card_transaction_adspend_charges()],
                            #         ]],
                            M("Aliexpressorder_event_update - Update",callback=lambda _=None:[Updater().Aliexpressorder_event_update(),self.set_menu()]),
                            # M("Update_TertiaryActions (headers: invoice_id, date, requires_response_by, status, order_problem, email, dispute_amount)",callback=lambda x:[setattr(x,"title","Update TertiaryActions - Running"),globalise(pool(lambda:Updater().Update_TertiaryActions()),"updater_update_tertiaryactions"),process(lambda:[setattr(x,"title","Update_TertiaryActions - Finished Running, Ready To Run") for i in range(WHILE_TRUE) if globe("updater_update_tertiaryactions").is_running() == False])]),
                            M("Add Payments (headers (if not PayPal/Stripe):id,created_at,amount,email,invoice_id,order_id,payment_gateway_name)",callback=lambda _=None:[Updater().Update_Payments(),self.set_menu()]),
                            M("Add Payouts (headers (if not PayPal/Stripe):id,created_at,amount,account_name,account_last_4_digits,payment_gateway_name)",callback=lambda _=None:[Updater().Update_Payouts(),self.set_menu()]),
                            [globalise(self,"verification_tests_x"),[M("Orders with seller not shipping goods ( Create ReOrder / Existing ReOrders / Pause All Adsets / Use Western Union )"), [[
                                                                          M("AliExpress Order %s (Reordered %sx)"%(
                                                                            i.id,
                                                                            or_list(lambda:len(Get(Aliexpressorder_event,id=i.id).reorder_ids),len([])))),
                                                                          [eval("""M("Create A Reorder",
                                                                            callback=lambda _=None:\
                                                                            [globalise(ReOrder().create(%s),"new_reorder"),
                                                                            Update(Get(Aliexpressorder_event,id=%s),
                                                                                reordered=True,
                                                                                reorder_ids=\
                                                                                  or_list(lambda:Get(Aliexpressorder_event,id=%s).reorder_ids+[globe("new_reorder").identifier],
                                                                                    lambda:[globe("new_reorder").identifier])),
                                                                            globe("verification_tests_x").set_menu()])"""%(i.id,i.id,i.id)),
                                                                          [M("Existing Reorders"),
                                                                          [M(i) for i in or_list(lambda:list(Get(Aliexpressorder_event,id=i.id).reorder_ids),[]) ]
                                                                          ]
                                                                          ]] for i in Filter(Aliexpressorder_event,event="Seller did not ship goods.",shop=Muta()().store_abbre)]]][1],
                            [globalise(self,"verification_tests_x"),[M("Orders cancelled due to security reasons ( Create ReOrder / Existing ReOrders / Pause All Adsets / Use Western Union )"), [[
                                                                          M("AliExpress Order %s (Reordered %sx)"%(
                                                                            i.id,
                                                                            or_list(lambda:len(Get(Aliexpressorder_event,id=i.id).reorder_ids),len([])))),
                                                                          [eval("""M("Create A Reorder",
                                                                            callback=lambda _=None:\
                                                                            [globalise(ReOrder().create(%s),"new_reorder"),
                                                                            Update(Get(Aliexpressorder_event,id=%s),
                                                                                reordered=True,
                                                                                reorder_ids=\
                                                                                  or_list(lambda:Get(Aliexpressorder_event,id=%s).reorder_ids+[globe("new_reorder").identifier],
                                                                                    lambda:[globe("new_reorder").identifier])),
                                                                            globe("verification_tests_x").set_menu()])"""%(i.id,i.id,i.id)),
                                                                          [M("Existing Reorders"),
                                                                          [M(i) for i in or_list(lambda:list(Get(Aliexpressorder_event,id=i.id).reorder_ids),[]) ]
                                                                          ]
                                                                          ]] for i in Filter(Aliexpressorder_event,event="Your payment was not processed due to security reasons. As a result your order has been cancelled. AliExpress did not accept any payment for this order. However, please note that some banks may hold onto payments for up to 3-15 business days.",shop=Muta()().store_abbre)]]][1],
                            M(""),
                          ]][1],
                        ],
                        ]
                        ],

                        # `it does not need to look @ activity. it has only to reposit, reverseretrospectively whoany.`
                        #[MenuItem("Active - Activity"),
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s %s <%s>", callback  = lambda _=None:   [self.set_menu(), [Update(i,active_status=False) for i in All(Activity)], Activity.start("%s"), self.set_menu(), 0/0]     )][1]"""%(i.name, ("(offchanced)" if i.offchanced == True else ""), ("TRUE" if i.active_status else("⁄")), i.name)) for i in All(Activity)  ],
                        #],
                        # (Seems Of Little Utility) Myticketrequest
                        #[setitem(g(),"Active - myticketrequest_x",self),[MenuItem("MyTicketRequest"), [MenuItem("+",callback=lambda _=None:[MyTicketRequest(request=OSA.display_dialog("request?")).save(),self.set_menu()] )]+[eval("""[exec("from rumps import MenuItem",globals()),[MenuItem("%s"),MenuItem("%s", callback=lambda _=None: [Update(Get(MyTicketRequest,request="%s"),response=OSA.display_dialog("response?: ")),g()["myticketrequest_x"].set_menu()]  )] ][1]""" % ( i.request,i.response,i.request,   )) for i in All(MyTicketRequest)]]][1],
                        
                        #(glanced at minimal thought sprouting utility)
                        #[MenuItem("Active - Proket"),x
                        #  [ MenuItem("+", callback=lambda _=None:[  setitem(g(),"x",OSA.display_dialog("Proket", [":)"]) ),redprint(g()["x"]), [Proket(proket=g()["x"]).save() for i in range(10) if len(Proket.objects.filter(proket=g()["x"]))==0]  ,  self.set_menu()]) ] + \
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s")][1]"""%(i.proket)) for i in All(Proket)  ],
                        #],
                        #[M("Active - 5. Unavailable Products"),
                        # [MenuItem("Active - 7. Routing (%s, (%s, %s), (%s, %s), %s)"%(len(onyx("e1",Muta()().store_abbre)),len([i for i in onyx("e2",Muta()().store_abbre) if i.calculate_time_so_far()<=20]),len([i for i in onyx("e2",Muta()().store_abbre) if i.calculate_time_so_far()>20]),len([i for i in onyx("e3",Muta()().store_abbre) if i.calculate_time_so_far()<=20]),len([i for i in onyx("e3",Muta()().store_abbre) if i.calculate_time_so_far()>20]), len(onyx("e4",Muta()().store_abbre)) )),
                        #   [keycall("calculate",Filter(Lineitem,shop=Muta()().store_abbre)),[
                        #     [b,[[M("%s (%s)"%(i,len([q for q in Filter(Lineitem,stage="%s"%(a),timesofar=(i),shop=Muta()().store_abbre)]))),[M("ID: %s"%(x.id)) for x in Filter(Lineitem,stage="%s"%(a),timesofar=(i),shop=Muta()().store_abbre)] ] for i in lrange(max(key("timesofar",Filter(Lineitem,shop=Muta()().store_abbre))+[0])+(1))]] for a,b in zip(["e1","e2","e3","e4"],["Ready To Order","Placed Order","Tracking And Shipping","Delivered"])
                        #   ]][1]
                        # ],



                        #translucience(),
                        #[MenuItem("Activity Cyclic"),
                        #  [ MenuItem("+", callback=lambda _=None:[  tryprocess(Activity_Cyclic(name=OSA.display_dialog("Name",[":)"]),cycle= OSA.display_dialog("Cycle",[":)"]),).save)  ,  self.set_menu()]) ] + \
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s %s", callback = lambda _=None: [Activity_Cyclic().start(name="%s")] )][1]"""%(i.name, ("(offchanced)" if i.active == True else ""), i.name)) for i in All(Activity_Cyclic) ] + \
                        #  [ process(lambda: [time.sleep( ((Date()+1).dateobj - (datetime.now()) ).seconds), Activity_Cyclic.iterate(), [[time.sleep(24*60*60),Activity_Cyclic.iterate()] for i in range(1000)]]) ],
                        #],
                        
                        #chilled
                        #slumbered (what am i gonna cheick names b4 i order?)
                        #[MenuItem("CNAMEKILL (slumbered)"),
                        #  [MenuItem(i.customer_name) for i in All(CNAMEKILL)]
                        #],

                        #[ eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s", callback=lambda: OSA().createnewarrangement("Profile\ 20", [0, 0, 922, 1200], 4, ["delay 1", "cmd_l", "delay 1", "%s", "return", "cmd_t", "cmd_l", "delay 1", ]))][1]"""%("%s-------------%s"%(i.customer_name,i.date), (Shop()(Get(Order,id=i.order_id).shop).Shopify_App_API_Url.split("@")[-1]+"/"+"orders"+"/"+"%s"%i.order_id))) for i in All(CNAMEKILL)  ],
                        #],

                        #[MenuItem("Combinations - Untagged"),
                        #  [ MenuItem("+", callback=lambda _=None:[  setitem(g(),"x",OSA.display_dialog("Untagged", ["careful"]) ),redprint(g()["x"]), [Combination(combination=g()["x"],slot="untagged").save() for i in range(10) if len(Combination.objects.filter(combination=g()["x"], slot="untagged"))==0]  ,  self.set_menu()]) ] + \
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem('''%s''')][1]"""%(i.combination)) for i in tcer(Filter(Combination, slot="untagged"))  ],
                        #],
                        #[MenuItem("LastCheckedTime"),
                        #  [MenuItem("🤾", callback=lambda _=None: [self.set_menu(),OSA().notify("Reset Menu! :)")] )] +\
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s",callback=lambda _=None:[pyperclip.copy("%s"),OSA().notify("Copied ID! :)")] )][1]"""%(i.X,i.X.split("__")[1]) ) for i in All(LastCheckedTime)  ],
                        #],
                        #products
                        # Programming_Glyph
                        #Proket
                        #Quote (unkerrolax)
                        #Ability
                        #[MenuItem("Records - Ability"),
                        #  New_Menulet.plus(lambda: [  setitem(g(),"x",OSA.display_dialog("Ability", [":)"]) ),redprint(g()["x"]), [Ability(ability=g()["x"]).save() for i in range(10) if len(Ability.objects.filter(ability=g()["x"]))==0]  ,  self.set_menu()], self) + \
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s")][1]"""%(i.ability)) for i in All(Ability)  ],
                        #],
                        #[MenuItem("Records - Angle"),
                        #  [ MenuItem("+", callback=lambda _=None:[Angle(date_added=datetime.now(),angle=OSA.display_dialog("Update?")).save(),self.set_menu()])]+\
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem('''%s: [%s]''',callback=lambda _=None:OSA.display_dialog('''%s'''))][1]"""%(i.date_added,i.angle,i.angle)) for i in tcer(All(Angle))  ],
                        #],
                        #[MenuItem("Records - Anglekeys"),
                        #  [ MenuItem("+", callback=lambda _=None:[Save(Anglekey,date_added=datetime.now(),anglekey=OSA.display_dialog("Angle Key")),self.set_menu()])] + \
                        #  [[MenuItem("%s"%(i)), [MenuItem("%s: %s"%(r.date_added, r.anglekey)) for r in [y for y in All(Anglekey) if y.anglekey.startswith("[%s]"%i)]]] for i in oset([re.findall(r"\[(.*?)\]",z)[0] for z in key("anglekey",All(Anglekey))])],
                        #],
                        #[M("Records - Supplies"), [M("+",callback=lambda _=None: [Save(Supplies,field=OSA.display_dialog("field?",default_answer=""),name=OSA.display_dialog("name?",default_answer=""),remaining=OSA.display_dialog("remaining?",default_answer=""),dollars=OSA.display_dialog("dollars?",default_answer=""),),self.set_menu()])]+[setitem(globals(),"supplies_x",self),[
                        #  [M("%s"%i),[[M("%s"%a.name), [M("-",callback=lambda _=None:[plusUpdate]), M("reset",callback=lambda _=None:[]), M("full reset",callback=lambda _=None:[])]] for a in Filter(Supplies,field="%s"%i)]] for i in sorted(set(key("field",All(Supplies))))
                        #  ]][1]
                        #],
                        [MenuItem("extended"), [
                        [MenuItem("Dump Database"),
                          [MenuItem("Dump Database", callback=lambda _=None: [SQL().dump_db_all(userfolder("~/tavern/tavern/soda/.%s.sql"%(datetime.now()))), OSA.notify("dumped at %s" % datetime.now())])]
                        ],
                        [MenuItem("fp"),
                          [eval("MenuItem('%s', callback=lambda _=None: os.system('/Applications/Firefox\ 65.app/Contents/MacOS/firefox -p %s &>/dev/null&') if not str('%s').endswith('Admin') else os.system('/Applications/Firefox\ 71.app/Contents/MacOS/firefox -p %s &>/dev/null&'))"%(i,i,i,i)) for i in sorted(lmap(lambda x: x.split(".")[1], os.listdir(GLOBAL_FIREFOX_PROFILE_PATH)))]
                        ],
                        [MenuItem("Records - Logins"),
                          [MenuItem("+", callback=lambda _,**kwargs: [[setitem(kwargs,"company",OSA.display_dialog("company?: ",default_answer="")), setitem(kwargs,"username",OSA.display_dialog("username?: ",default_answer="")), setitem(kwargs,"password",OSA.display_dialog("password?: ",default_answer="",hidden=True)), Save(Password,company=kwargs["company"],username=kwargs["username"],password=kwargs["password"])if(len(Filter(Password,company=kwargs["company"],username=kwargs["username"]))==0)else(Update(Get(Password,company=kwargs["company"],username=kwargs["username"]),password=kwargs["password"]))], self.set_menu()])] + \
                          #[[MenuItem("%s"%a), [eval("MenuItem('%s', callback=lambda _=None:(lambda x: [[[OSA.notify(str(i)),sp(1)] for i in tcer(range(1,4))],[[OSA(None,[i]),sp(random.uniform(0.25,0.4))] for i in x]])(Get(Password,company='%s',username='%s').password))"%(b.username,b.company,b.username)) for b in Filter(Password,company=a)]] for a in sorted(set(key("company", All(Password))))]
                          [[MenuItem("%s"%a), [eval("MenuItem('%s', callback=lambda _=None:pyperclip.copy(Get(Password,company='%s',username='%s').password))"%(b.username,b.company,b.username)) for b in Filter(Password,company=a)]] for a in sorted(set(key("company", All(Password))))]
                        ],
                        # [MenuItem("Records - Binarydata"), # Binarydata
                        #   [MenuItem("+", callback=lambda _=None:[Binarydata().update_or_create(OSA.display_dialog("File?: ")), self.set_menu()] )] + \
                        #   [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s",callback=lambda _=None: [Binarydata().export(Get(Binarydata,id=%s).filename,OSA.display_dialog("Export Path?: ")),""] ) ][1]"""%(i.filename, i.id, )) for i in All(Binarydata)  ],
                        # ],

                        #[MenuItem("Records - BusinessQuotes"),
                        #  [ MenuItem("+", callback=lambda _=None:[  setitem(g(),"x",OSA.display_dialog("BusinessQuote", [":)"]) ),redprint(g()["x"]), [BusinessQuote(businessquote=g()["x"]).save() for i in range(10) if len(BusinessQuote.objects.filter(businessquote=g()["x"]))==0]  ,  self.set_menu()]) ] + \
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s")][1]"""%(i.businessquote)) for i in All(BusinessQuote)  ],
                        #],
                        #[MenuItem("Records - Essays"),
                        #  [ MenuItem("+", callback=lambda _=None: [Essay(title=OSA.display_dialog("title?", ["OK"]), essay=OSA.display_dialog("essay?",["OK"]) ).save(),self.set_menu()] ) ] +\
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s", callback=lambda _=None: [OSA.display_dialog((Get(Essay,title="%s").essay))]   )][1]"""%( i.title , i.title )) for i in keysort("title",All(Essay),tcer=False)  ],
                        #],
                        #[MenuItem("Records - ExecutableText"),
                        #  [ MenuItem("+", callback=lambda _=None:[  setitem(g(),"x",pyperclip.paste() ),redprint(g()["x"]), [ExecutableText(w=g()["x"]).save() for i in range(10) if len(ExecutableText.objects.filter(w=g()["x"]))==0]  ,  self.set_menu()]) ] + \
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s", callback=lambda _=None: [pyperclip.copy(Get(ExecutableText,w="%s").x),OSA().notify("pyperclipped")]   )][1]"""%( i.w , i.w )) for i in keysort("w",All(ExecutableText),tcer=False)  ],
                        #],
                        #[MenuItem("Records - Grammar"),
                        #  [ MenuItem("+", callback=lambda _=None:[  setitem(g(),"x",OSA.display_dialog("Grammar", [":)"]) ),redprint(g()["x"]), [Grammar(grammar=g()["x"]).save() for i in range(10) if len(Grammar.objects.filter(grammar=g()["x"]))==0]  ,  self.set_menu()]) ] + \
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s", callback=lambda _=None:OSA.display_dialog(q=Get(Grammar,id=%s).grammar))][1]"""%(i.grammar,i.id)) for i in All(Grammar)  ],
                        #],
                        #[MenuItem("Records - Joke"),
                        #  [ MenuItem("+", callback=lambda _=None:[  setitem(g(),"x",OSA.display_dialog("A Fine Joke", [":)"]) ),redprint(g()["x"]), [Joke(joke=g()["x"]).save() for i in range(10) if len(Joke.objects.filter(joke=g()["x"]))==0]  ,  self.set_menu()]) ] + \
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s")][1]"""%(i.joke)) for i in All(Joke)  ],
                        #],
                        #[MenuItem("Records - Level_Eleven_Bugs"),
                        #  [setitem(g(),"level_eleven_bugs_x",self),[ MenuItem("+", callback=lambda _=None: [Level_Eleven_Bugs(level_eleven_bug=OSA.display_dialog("YeS SiR",buttons=["OK"]),first_encounter=Date().Now()).save(), g()["level_eleven_bugs_x"].set_menu()])]]   [1] + \
                        #  [MenuItem("[%s][%s]"%(i.first_encounter,i.level_eleven_bug)) for i in All(Level_Eleven_Bugs) ],
                        #],
                        #[MenuItem("Records - Questionnaires"),
                        #  [ MenuItem("+ (on_clipboard)", callback=lambda _=None:[ Questionnaire(questionnaire=pyperclip.paste() ).save(), self.set_menu() ]) ] + \
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s", callback=lambda _=None: OSA.display_dialog(default_answer=Get(Questionnaire,id=%s).questionnaire, buttons=[":)"]) )][1]"""%(i.id, i.id)) for i in All(Questionnaire)  ],
                        #],
                        #[MenuItem("Records - Quotes"),
                        #  [ MenuItem("+", callback=lambda _=None:[  setitem(g(),"x",OSA.display_dialog("Quote", [":)"]) ),redprint(g()["x"]), [Quote(quote=g()["x"]).save() for i in range(10) if len(Quote.objects.filter(quote=g()["x"]))==0]  ,  self.set_menu()]) ] + \
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s")][1]"""%(i.quote)) for i in All(Quote)  ],
                        #],
                        #[MenuItem("Records - Reminders"),
                        #  [ MenuItem("+", callback=lambda _=None:[  setitem(g(),"x",OSA.display_dialog("A Sweet Reminder", [":)"]) ),redprint(g()["x"]), [Reminder(reminder=g()["x"]).save() for i in range(10) if len(Reminder.objects.filter(reminder=g()["x"]))==0]  ,  self.set_menu()]) ] + \
                        #  [ eval("""[exec("from rumps import MenuItem",globals()),MenuItem('''%s''',callback=lambda _=None:[OSA.notify(i.reminder),pyperclip.copy(i.reminder),OSA.notify("pyperclipped")])][1]"""%(i.reminder)) for i in tcer(All(Reminder))  ],
                        #],
                        #(MenuItem("Records - Size ()"), [[ [Size().add().ensure_existing_measurement_today(),MenuItem("%s"%i.date)][1], [MenuItem("0. toothbrushes: %s" % i.toothbrushes    ,    callback = lambda _ = None:                                              [Size().add().toothbrushes()  ,  self.set_menu()]                       ),MenuItem("1. showers: %s" % i.showers    ,    callback = lambda _ = None:                                              [Size().add().showers()  ,  self.set_menu()]                       ),MenuItem("2. food: %s" % i.food    ,    callback = lambda _ = None:                                              [Size().add().food()  ,  self.set_menu()]                       ),MenuItem("3. weight: %s" % i.weight    ,    callback = lambda _ = None:                                              [Size().add().weight()  ,  self.set_menu()]                       ),MenuItem("4. thigh_size: %s" % i.thigh_size    ,    callback = lambda _ = None:                                              [Size().add().thigh_size()  ,  self.set_menu()]                       ),MenuItem("5. calf_size: %s" % i.calf_size    ,    callback = lambda _ = None:                                              [Size().add().calf_size()  ,  self.set_menu()]                       ),MenuItem("6. gluteus_size: %s" % i.gluteus_size    ,    callback = lambda _ = None:                                              [Size().add().gluteus_size()  ,  self.set_menu()]                       ),MenuItem("7. stomach_size: %s" % i.stomach_size    ,    callback = lambda _ = None:                                              [Size().add().stomach_size()  ,  self.set_menu()]                       ),MenuItem("8. chest_size: %s" % i.chest_size    ,    callback = lambda _ = None:                                              [Size().add().chest_size()  ,  self.set_menu()]                       ),MenuItem("9. hydromaxes: %s" % i.hydromaxes    ,    callback = lambda _ = None:                                              [Size().add().hydromaxes()  ,  self.set_menu()]                       ),MenuItem("10. jelqs: %s" % i.jelqs    ,    callback = lambda _ = None:                                              [Size().add().jelqs()  ,  self.set_menu()]                       ),MenuItem("11. penis_size: %s" % i.penis_size    ,    callback = lambda _ = None:                                              [Size().add().penis_size()  ,  self.set_menu()]                       ),MenuItem("12. morning_setup: %s" % i.morning_setup    ,    callback = lambda _ = None:                                              [Size().add().morning_setup()  ,  self.set_menu()]                       ),MenuItem("14. morning_wakeup_time: %s" % i.morning_wakeup_time    ,    callback = lambda _ = None:                                              [Size().add().morning_wakeup_time()  ,  self.set_menu()]                       ),MenuItem("15. punches: %s" % i.punches    ,    callback = lambda _ = None:                                              [Size().add().punches()  ,  self.set_menu()]                       ),MenuItem("16. kicks: %s" % i.kicks    ,    callback = lambda _ = None:                                              [Size().add().kicks()  ,  self.set_menu()]                       ),MenuItem("17. circles: %s" % i.circles    ,    callback = lambda _ = None:                                              [Size().add().circles()  ,  self.set_menu()]                       ),MenuItem("18. new_feints: %s" % i.new_feints    ,    callback = lambda _ = None:                                              [Size().add().new_feints()  ,  self.set_menu()]                       ),MenuItem("19. crunches: %s" % i.crunches    ,    callback = lambda _ = None:                                              [Size().add().crunches()  ,  self.set_menu()]                       ),MenuItem("20. pullups: %s" % i.pullups    ,    callback = lambda _ = None:                                              [Size().add().pullups()  ,  self.set_menu()]                       ),MenuItem("21. dips: %s" % i.dips    ,    callback = lambda _ = None:                                              [Size().add().dips()  ,  self.set_menu()]                       ),MenuItem("22. pants_left: %s" % i.pants_left   ,    callback = lambda _= None:  [Size().add().pants_left()  ,  self.set_menu()]    ),MenuItem("23. shirts_left: %s" % i.shirts_left   ,    callback = lambda _= None:  [Size().add().shirts_left()  ,  self.set_menu()]    ),MenuItem("24. mood: %s" % i.mood   ,    callback = lambda _= None:  [Size().add().mood()  ,  self.set_menu()]    ),MenuItem("25. shaved: %s" % i.shaved   ,    callback = lambda _= None:  [Size().add().shaved()  ,  self.set_menu()]    ),MenuItem("26. skyrocket: %s" % i.skyrocket    ,    callback = lambda _ = None:                                              [Size().add().skyrocket()  ,  self.set_menu()]                       ),MenuItem("27. are_you_rigged_to_upwork: %s" % i.are_you_rigged_to_upwork    ,    callback = lambda _ = None:                                              [Size().add().are_you_rigged_to_upwork()  ,  self.set_menu()]                       ), MenuItem("28. emails: %s" % i.emails    ,    callback = lambda _ = None:                                              [Size().add().emails()  ,  self.set_menu()]                       ),    MenuItem("29. estimated_humorisms: %s" % i.estimated_humorisms    ,    callback = lambda _ = None:                                              [Size().add().estimated_humorisms()  ,  self.set_menu()]                       ),    ]   ] for i in  tcer(All(Size)) ]
                        #),


                        # [MenuItem("Records - Meals (%s Today)"%(len(Filter(Meal,time__range=[(Date().datestr),(Date().datestr)])))),
                        #   [
                        #     [M("Mealinventory"), [M("+",callback=lambda _=None:[Mealinventory().add(x=OSA.display_dialog("format (separate by commas): # meal @ price, # meal2 @ price\nexample: 16 jelly @ 0.05, 16 pb @ 0.05")),self.set_menu()])]+[i for i in sorted(flatten(lmap(Mealinventory().giveformat,sorted(set(key("name",All(Mealinventory))))),1))]],
                        #     [M("eat"), [M("+",callback=lambda _=None:[Meal().add(x=OSA.display_dialog("format (separate by commas): # meal, # meal2\nexample: 16 jelly, 16 pb")),self.set_menu()])]+["Meal: %s %s on %s ($%s)"%(int(i.ounces), i.name, Date().friendlydate(i.time), round(i.price,2)) for i in tcer(All(Meal))]],
                        #   ]
                        # ],

                        # [MenuItem("Records - Typing Format"),
                        #   [
                        #     [M("Variable: %s"%(Typing_Format()().variable)),[eval("""M("%s",callback=lambda _=None:[Update(Typing_Format()(),variable="%s"),self.set_menu()])"""%(i,i)) for i in ["Start with `a`", "Start with `i`"] ]],     [M("Save Lines: %s"%((("Do")if(Typing_Format()().save_lines)else("Don't")))),[eval("""M("%s",callback=lambda _=None:[Update(Typing_Format()(),save_lines=eval("%s")),self.set_menu()])"""%(i,i)) for i in ["True", "False"] ]],     [M("Verbal: %s"%(Typing_Format()().verbal)),[eval("""M("%s",callback=lambda _=None:[Update(Typing_Format()(),verbal="%s"),self.set_menu()])"""%(i,i)) for i in [50, 75, 90] ]],     [M("Print: %s"%((("Do")if(Typing_Format()().printful)else("Don't")))),[eval("""M("%s",callback=lambda _=None:[Update(Typing_Format()(),printful=eval("%s")),self.set_menu()])"""%(i,i)) for i in ["True", "False"] ]],     [M("Naming: %s"%(Typing_Format()().naming)),[eval("""M("%s",callback=lambda _=None:[Update(Typing_Format()(),naming="%s"),self.set_menu()])"""%(i,i)) for i in ["Important", "Not Important"] ]],     [M("Naming Collision: %s"%(Typing_Format()().naming_collision)),[eval("""M("%s",callback=lambda _=None:[Update(Typing_Format()(),naming_collision="%s"),self.set_menu()])"""%(i,i)) for i in ["Important", "Not Important"] ]],     [M("Rudeness: %s"%(Typing_Format()().rudeness)),[eval("""M("%s",callback=lambda _=None:[Update(Typing_Format()(),rudeness="%s"),self.set_menu()])"""%(i,i)) for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] ]],     [M("Pseudocode: %s"%((("Do")if(Typing_Format()().pseudocode)else("Don't")))),[eval("""M("%s",callback=lambda _=None:[Update(Typing_Format()(),pseudocode=eval("%s")),self.set_menu()])"""%(i,i)) for i in ["True", "False"] ]],     [M("Depth of Recursion: %s"%(Typing_Format()().depth_of_recursion)),[eval("""M("%s",callback=lambda _=None:[Update(Typing_Format()(),depth_of_recursion="%s"),self.set_menu()])"""%(i,i)) for i in [1, 2, 3, 4] ]],     [M("Ugliness: %s"%((("Do")if(Typing_Format()().ugliness)else("Don't")))),[eval("""M("%s",callback=lambda _=None:[Update(Typing_Format()(),ugliness=eval("%s")),self.set_menu()])"""%(i,i)) for i in ["True", "False"] ]],     [M("Error Method: %s"%(Typing_Format()().error_method)),[eval("""M("%s",callback=lambda _=None:[Update(Typing_Format()(),error_method="%s"),self.set_menu()])"""%(i,i)) for i in ["Discover", "Plan First"] ]],
                        #   ]
                        # ],

                        # [MenuItem("Records - Degradantlist"),
                        #   [ MenuItem("+", callback=lambda _=None:[setitem(g(),"degradantlist_list_self",self),Degradantlist(degradantlist=OSA.display_dialog("Degradantlist", ["OK"]),is_completed=False).save(),g()["degradantlist_list_self"].set_menu()]) ] + \
                        #   [[MenuItem("Done"),[MenuItem(i.degradantlist) for i in Filter(Degradantlist,is_completed=1)]]]+[ [setitem(g(),"degradantlist_list_self",self),eval("""[exec("from rumps import MenuItem",globals()),MenuItem('''%s''', callback=lambda _=None: [Update (Get(Degradantlist,id=%s),is_completed=True )  ,  g()["degradantlist_list_self"].set_menu()]   )][1]"""%(i.degradantlist,  i.id, ))][1] for i in Filter(Degradantlist,is_completed=False)  ],
                        # ],
                        # [MenuItem("Records - To Do List"),
                        #   [ MenuItem("+", callback=lambda _=None:[  setitem(g(),"x",OSA.display_dialog("Todo", [":)"]) ),setitem(g(),"xx",OSA.display_dialog("pyperclips (or None)", [":)"]) ),redprint(g()["x"]), [Todo(todo=g()["x"],pyperclips=g()["xx"],is_completed=False).save() for i in range(10) if len(Todo.objects.filter(todo=g()["x"],is_completed=False))==0]  ,  self.set_menu()]) ] + \
                        #   [[MenuItem("Done"),[MenuItem(i.todo) for i in Filter(Todo,is_completed=1)]]]+[ [setitem(g(),"todo_list_self",self),eval("""[exec("from rumps import MenuItem",globals()),MenuItem("%s", callback=lambda _=None: [Update (Get(Todo,id=%s),is_completed=True )  ,  g()["todo_list_self"].set_menu()]   )][1]"""%(i.todo,  i.id, ))][1] for i in Filter(Todo,is_completed=False)  ],
                        # ],
                        # [MenuItem("Records - Pyperclips"),
                        #   [ MenuItem("+", callback=lambda _=None:[Pyperclip(pyperclip=OSA.display_dialog("Pyperclip?",default_answer="")).save(),self.set_menu()])] + \
                        #   [globalise(self,"pyperclip_x"),[[M("View"),[[M(i.pyperclip), eval("""[M("To Clip",callback=lambda _=None:[pyperclip.copy(Get(Pyperclip,id=%s).pyperclip)]),M("Delete",callback=lambda _=None:[Del(Get(Pyperclip,id=%s)),g()["pyperclip_x"].set_menu()]),M("Update",callback=lambda _=None:[Update(Get(Pyperclip,id=%s),pyperclip=OSA.log("pyperclip?")),g()["pyperclip_x"].set_menu()])]"""%(i.id,i.id,i.id))]]] for i in tcer(All(Pyperclip))]][1]
                        # ],
                        # [MenuItem("Records - Unsolvable Problems"),
                        #   [MenuItem("+",callback=lambda _=None:[Save(UnsolvableProblem,unsolvableproblem=OSA.display_dialog("Unsolvable Problem?")),self.set_menu()])] + \
                        #   [eval("""MenuItem('''%s''', callback = lambda _=None:[OSA.display_dialog('''%s''')])"""%(i.unsolvableproblem,i.unsolvableproblem)) for i in tcer(All(UnsolvableProblem))]
                        # ],
                        # [MenuItem("Records - Adstips"),
                        #   [ MenuItem("+", callback=lambda _=None:[Adstip(adstip=OSA.display_dialog("Ads tip?",default_answer="")).save(),self.set_menu()])] + \
                        #   [ eval("""[exec("from rumps import MenuItem",globals()),[MenuItem('''View'''), MenuItem('''%s''',callback=lambda _=None:[OSA.notify(i.adstip)])] ][1]"""%(i.adstip)) for i in tcer(All(Adstip))  ],
                        # ],
                        # [MenuItem("Records - Tipsingeneral"),
                        #   [ MenuItem("+", callback=lambda _=None:[Tipsingeneral(tipsingeneral=OSA.display_dialog("Tip in general?",default_answer="")).save(),self.set_menu()])] + \
                        #   [ eval("""[exec("from rumps import MenuItem",globals()),[MenuItem('''View'''), MenuItem('''%s''',callback=lambda _=None:[OSA.notify(i.tipsingeneral)])] ][1]"""%(i.tipsingeneral)) for i in tcer(All(Tipsingeneral))  ],
                        # ],

                        #[MenuItem("Binarydata"),
                        #  [ MenuItem("+", callback=lambda _=None:[  setitem(g(),"x",OSA.display_dialog("Dictionary Entry", ["careful"]) ),redprint(g()["x"]), [Dictionaryentry(word=g()["x"]).save() for i in range(10) if len(Dictionaryentry.objects.filter(word=g()["x"]))==0]  ,  self.set_menu()]) ] + \
                        #

                        # [MenuItem("Records - Dictionary Entry"),
                        #   [ MenuItem("+", callback=lambda _=None:[  [setitem(g(),"x",OSA.display_dialog("Dictionary Entry", ["careful"]) ),setitem(g(),"y",OSA.display_dialog("Definition", ["careful"]) )],redprint(g()["x"]),redprint(g()["y"]), [Dictionaryentry(word=g()["x"],definition=g()["y"]).save() for i in range(10) if len(Dictionaryentry.objects.filter(word=g()["x"]))==0]  ,  self.set_menu()  ]) ] + \
                        #   [ [setitem(g(),"dictionaryentry_self",self),eval("""[exec("from rumps import MenuItem",globals()),[MenuItem('''[ [ [ [ [     %s     ] ] ] ] ]:%s (Videod: %s)''', callback=lambda _=None: [setitem(g(),"dictionaryentry_x",OSA.display_dialog('''%s''',['OK']))  ,  ([Update(Get(Dictionaryentry,id=%s),videod=True)  ,  OSA().notify("videod")  ,  time.sleep(2),redprint(self)  , g()["dictionaryentry_self"].set_menu()  ])if("Videod"==g()["dictionaryentry_x"])else(OSA().notify("not videod"))  ]   ),[M(i) for i in Get(Dictionaryentry,id=%s).definition.replace("\\n"," ").split(" ")]+[M(" ")]+[M("%s",callback=lambda _=None:[setitem(g(),"dictionaryentry_x",OSA.display_dialog('''%s''',['OK']))  ,  ([Update(Get(Dictionaryentry,id=%s),videod=True)  ,  OSA().notify("videod")  ,  time.sleep(2),redprint(self)  , g()["dictionaryentry_self"].set_menu()  ])if("Videod"==g()["dictionaryentry_x"])else(OSA().notify("not videod"))  ])]]][1]"""%( " ".join(i.word.upper()) , i.definition,         i.videod            , i.definition  ,  i.id  ,  i.id  ,  i.word.upper(),i.definition,i.id ))][1] for i in tcer(All(Dictionaryentry))  ],
                        # ],
                        [M("Updates"),[M("%s: %s"%(Date().friendlydate(i.time),i.name)) for i in keysort("time",All(Updates))]],

                        [MenuItem("Work Mode - %s"%([Update(Muta()(),sciencevessels_on=False)if(Muta()().sciencevessels_on==True and Muta()().fig_on==True)else(),("Fig")if(Muta()().fig_on)else("AddProducts")if(Muta()().addproducts_on)else("ScienceVessels")if(Muta()().sciencevessels_on)else("Support")if(Muta()().support_on)else("Job Search")if(Muta()().job_search_on)else("Incept Products")if(Muta()().incept_product_on)else("ProductChange")if(Muta()().productchange_on)else(None)][1])),
                          [MenuItem("Help",callback=lambda _=None:[OSA.display_dialog("Use ScienceVessels to add to a list of products and then send them to the shop all at once or use Fig to add products individually.",text_prompt=False),self.set_menu()]),
                          ["Workmode", [M("Fig",callback=lambda _=None:[Update(Muta()(),**{"fig_on":1,"addproducts_on":0,"sciencevessels_on":0,"support_on":0,"job_search_on":0,"incept_product_on":0,"productchange_on":0,}),self.set_menu()]),M("AddProducts",callback=lambda _=None:[Update(Muta()(),**{"fig_on":0,"addproducts_on":1,"sciencevessels_on":0,"support_on":0,"job_search_on":0,"incept_product_on":0,"productchange_on":0,}),self.set_menu()]),M("ScienceVessels",callback=lambda _=None:[Update(Muta()(),**{"fig_on":0,"addproducts_on":0,"sciencevessels_on":1,"support_on":0,"job_search_on":0,"incept_product_on":0,"productchange_on":0,}),self.set_menu()]),M("Support",callback=lambda _=None:[Update(Muta()(),**{"fig_on":0,"addproducts_on":0,"sciencevessels_on":0,"support_on":1,"job_search_on":0,"incept_product_on":0,"productchange_on":0,}),self.set_menu()]),M("Job Search",callback=lambda _=None:[Update(Muta()(),**{"fig_on":0,"addproducts_on":0,"sciencevessels_on":0,"support_on":0,"job_search_on":1,"incept_product_on":0,"productchange_on":0,}),self.set_menu()]),M("Incept Products",callback=lambda _=None:[Update(Muta()(),**{"fig_on":0,"addproducts_on":0,"sciencevessels_on":0,"support_on":0,"job_search_on":0,"incept_product_on":1,"productchange_on":0,}),self.set_menu()]),M("Product Change",callback=lambda _=None:[Update(Muta()(),**{"fig_on":0,"addproducts_on":0,"sciencevessels_on":0,"support_on":0,"job_search_on":0,"incept_product_on":0,"productchange_on":1,}),self.set_menu()])]]],
                        ],

                        # [MenuItem("AddProducts (%s)"%(("On")if(Muta()().addproducts_on==True)else("Off"))),
                        #   [
                        #   MenuItem("Send products",callback=lambda _=None:[OSA.log("Opening urls for %s products. Please open a Google Chrome browser window to open the urls."%(len(Filter(AddProduct,sent=0))),tp=False),keycall("send",Filter(AddProduct,sent=0)),self.set_menu()] ),
                        #   MenuItem("Refresh",callback=lambda _=None:self.set_menu()),
                        #   *[MenuItem(i.x) for i in Filter(AddProduct,sent=0)],
                        #   ]
                        # ],

                        # [MenuItem("ScienceVessels (%s)"%(("On")if(Muta()().sciencevessels_on==True)else("Off"))),
                        #   [
                        #   MenuItem("Send products",callback=lambda _=None:[OSA.log("Opening urls for %s products. Please open a Google Chrome browser window to open the urls."%(len(Filter(AddProduct,sent=0))),tp=False),keycall("warp",Filter(ScienceVessel,warped=0)),self.set_menu()] ),
                        #   MenuItem("Refresh",callback=lambda _=None:self.set_menu()),
                        #   *[MenuItem(i.x) for i in Filter(ScienceVessel,warped=0)],
                        #   ]
                        # ],

                        # [M("Nichelet"),[M("",icon=[globalise(get_random_address(userfolder("~/tavern/tavern/soda/dls")).png(),"icon_image_x"),open(globe("icon_image_x"),"wb").write(i.icon_image),globe("icon_image_x")][-1],callback=lambda _=None:[]) for i in Filter(Product,product_type=Muta()().niche)]],
                        [M("Use Shops Menulet"), M("Use Shops Menulet", callback=lambda _=None:[tryprocess(lambda:Ryle())])],

                        [M("Update Lineitem Addresses for an Order"),M("Update Lineitem Addresses for an Order",callback=lambda _=None:[update_address()])],
                        [M("Get Tracking Number"),M("Get Tracking Number",callback=lambda _=None:[OSA.log("Here is the tracking number",df=alitracker(*OSA.log("Shop and order number (delimted by ', ')?").split(", ")))] )],
                        [M("Got Ali Url"),M("Got Ali Url",callback=lambda _=None:[got_ali_url()])],
                        [M("Bitly Url"),M("Bitly Url",callback=lambda _=None:[pyperclip.copy(bitly_url(pyperclip.paste()))])],
                        [M("Message Game"),M("Message Game",callback=lambda _=None:[process(lambda:Message_Game().add())])],
                        [M("Add Content"),M("Add Content",callback=lambda _=None:[process(lambda:Content().add_content() )])],
                        [M("Post Content"),M("Post Content",callback=lambda _=None:[process(lambda:Content()() )])],
                        [M("Adjust Ad Columns"),M("Adjust Ad Columns",callback=lambda _=None:[process(lambda:adjust_ad_columns() )])],
                        # [MenuItem("spare time functions"),
                        #   [
                        #   [M("SoundFiles"), [
                        #                         [M("Saved"),
                        #                           [eval("""M("%s",callback=lambda _=None:[Binarydata().export( userfolder("~/tavern/tavern/soda/%s") ),process(lambda:[os.system("afplay '''~/tavern/tavern/soda/%s'''"),os.remove(userfolder("~/tavern/tavern/soda/%s"))])])"""%(i.filename,i.filename,i.filename,i.filename)) for i in Filter(Binarydata,filename__endswith=".wav")]],
                        #                       M(("Record")if(len([i for i in os.listdir(userfolder("~/tavern/tavern"))if(i.endswith(".wav"))])==0)else("Stop Recording"),callback=lambda _=None:(globalise(process(lambda: [globalise(userfolder("~/tavern/tavern/%s.wav"%(datetime.now())),"fig_soundfiles_x_datetime"),os.system("/usr/local/bin/sox -d '%s'&>/dev/null&"%(globe("fig_soundfiles_x_datetime"))),self.set_menu()]),"fig_soundfiles_x"))if(len([i for i in os.listdir(userfolder("~/tavern/tavern")) if i.endswith(".wav")])==0)else([Binarydata().update_or_create([i for i in os.listdir(userfolder("~/tavern/tavern")) if i.endswith(".wav")][0]),globalise(None,"fig_soundfiles_x"),self.set_menu()]) ),
                        #                     ]],
                        #   [M("Screencasts"), [
                        #                         [M("Saved"),
                        #                           [eval("""M("%s",callback = lambda _=None: [Binarydata().export("%s")])"""%(i.filename,i.filename)) for i in Filter(Binarydata,filename__endswith=".mov")]],
                        #                       M("Record",callback = lambda _=None:[os.chdir(userfolder("~/tavern/tavern")),process(quicktime_recording)]),
                        #                       M("Save", callback = lambda _=None:[os.chdir(userfolder("~/Documents")),exec("import shutil",globals()),globalise(("%s.mov"%(datetime.now())),"fig_screencasts_x"),shutil.move([i for i in os.listdir() if i.endswith(".mov")][0],globe("fig_screencasts_x")),Binarydata().update_or_create(globe("fig_screencasts_x")),self.set_menu()])
                        #                     ]],
                        #   [M("Help"),[M("1. Title"),M("2. Image IDX"),M("3. Image Indexes"),M("4. Option Indexes"),M("5. Variant Indexes"),M("6. Size Chart"),M("7. Description"),]],
                        #   [M("Use Shops Menulet"), M("Use Shops Menulet", callback=lambda _=None:[tryprocess(lambda:Ryle())])],
                        #   [M("Get Product Source Mode - %s"%(Muta()().get_product_source_mode)),[M("Use Requests (A Python HTTP library)",callback=lambda _=None:[Update(Muta()(),get_product_source_mode="Requests"),self.set_menu()]),M("Read Browser HTML Page Source",callback=lambda _=None:[Update(Muta()(),get_product_source_mode="Read Browser HTML Page Source"),self.set_menu()])]],
                        #   [M("Product Adding Mode - %s"%(Muta()().product_adding_mode)), [M("Normal",callback=lambda _=None:[Update(Muta()(),product_adding_mode="Normal"), self.set_menu()]),M("Convoluted",callback=lambda _=None:[Update(Muta()(),product_adding_mode="Convoluted"),self.set_menu()])]],
                        #   [M("Run Export"), M("Run Export", callback=lambda _=None:[globalise(OSA.log("Please select from the following to export to a csv file.\n\n1. Adset_duplicate\n2. Adsethourlyinsight\n3. Adsethourlyinsightdata\n4. Adsetinsight\n5. Aliexpressorder\n6. Aliexpressorder_event\n7. ApprovedTransaction\n8. Audience\n9. CruxSupplier\n10. Facebookadaccountspend\n11. Facebookkeyword\n12. Facebookkeywordlist\n13. Facebookpage\n14. InceptedProduct\n15. Interest\n16. Interestinsight\n17. Lineitem\n18. New_Email\n19. New_Email_Template\n20. Niche\n21. PaidCardNumber\n22. PriceDecrease\n23. PriceIncrease\n24. ProductTalk\n25. ReOrder\n26. ScienceVessel\n27. SecondaryAction\n28. Settlement\n29. Subscription\n30. TertiaryAction\n31. TertiaryAction_Template\n32. AceInTheHole\n33. Adset\n34. Order\n35. Product"),"run_export_x"),SQL().table_to_xlsx("soda",globe("run_export_x"),(userfolder("~/tavern/tavern/%s.xlsx"%(globe("run_export_x")))) ),OSA.log("Your export can be found at /Users/<your user name>/tavern/tavern/%s.xlsx."%(globe("run_export_x")),tp=False)])],
                        #   [M("Run Command"), M("Run Command",callback=lambda _=None:[process(lambda: exec(OSA.log("Command?:")))])],
                        #   [M("Encoding"),M("Run",callback=lambda _=None:[pyperclip.copy(pyperclip.paste().encode("ascii",errors="backslashreplace").decode())])],
                        #   M("Run chromejstest",callback=lambda _=None:process(lambda:chromejstest()) ),
                        #   [M("Update Lineitem Addresses for an Order"),M("Update Lineitem Addresses for an Order",callback=lambda _=None:[update_address()])],
                        #   [M("Export A Video"),M("Export A Video",callback=lambda _=None:[export_a_video()])],
                        #   [setattr(self,"is_repeat",getattr(self,"is_repeat",False)),["Timer", [
                        #                           MenuItem("Is_Repeat %s"%("On"if(self.is_repeat)else("Off")),callback=lambda _=None:[setattr(self,"is_repeat",not self.is_repeat),self.set_menu()]),
                        #                           MenuItem("1:00",callback=lambda _=None:process(lambda: [[[[setattr(self.app,"title","%s:%s" % (int((60-i)/60), str((60-i)%60).zfill(2) )),zz(1)] for i in range(61)] for i in range(1 if self.is_repeat == False else WHILE_TRUE)],setattr(self.app,"title","🥃")] )),
                        #                           MenuItem("2:00",callback=lambda _=None:process(lambda: [[[[setattr(self.app,"title","%s:%s" % (int((120-i)/60), str((120-i)%60).zfill(2) )),OSA.notify("%s:%s" % (int((120-i)/60), str((120-i)%60).zfill(2) )) if self.notify == 1 else(),zz(1)] for i in range(121)] for i in range(1 if self.is_repeat == False else WHILE_TRUE)],setattr(self.app,"title","🥃")] )),
                        #                           MenuItem("4:00",callback=lambda _=None:process(lambda: [[[[setattr(self.app,"title","%s:%s" % (int((240-i)/60), str((240-i)%60).zfill(2) )),OSA.notify("%s:%s" % (int((240-i)/60), str((240-i)%60).zfill(2) )) if self.notify == 1 else(),zz(1)] for i in range(241)] for i in range(1 if self.is_repeat == False else WHILE_TRUE)],setattr(self.app,"title","🥃")] )),
                        #                           MenuItem("10:00",callback=lambda _=None:process(lambda: [[[[setattr(self.app,"title","%s:%s" % (int((600-i)/60), str((600-i)%60).zfill(2) )),OSA.notify("%s:%s" % (int((600-i)/60), str((600-i)%60).zfill(2) )) if self.notify == 1 else(),zz(1)] for i in range(601)] for i in range(1 if self.is_repeat == False else WHILE_TRUE)],setattr(self.app,"title","🥃")] )),
                        #                           MenuItem("Set Timer", callback = lambda _=None: process(lambda: [globalise(datetime.strptime(OSA.display_dialog("Alarm Timer? In format Day of week, Hour of day, Minute of the hour, AM/PM")+ (", ") + ("%s, %s, %s"%(datetime.now().year,datetime.now().month,datetime.now().day)),"%A, %I, %M, %p, %Y, %m, %d"),"menulet_timer_alarm"),[[([[os.system("osascript -e 'set Volume 10'"),os.system("afplay /System/Library/Sounds/Submarine.aiff -v 10 &"),time.sleep(0.5)] for i in range(WHILE_TRUE)]) if( ((globe("menulet_timer_alarm").weekday()==datetime.now().weekday())and(globe("menulet_timer_alarm").hour==datetime.now().hour)and(globe("menulet_timer_alarm").minute==datetime.now().minute)) )else(),time.sleep(30)] for i in range(WHILE_TRUE)],self.set_menu()])),
                        #                         ]]] [1]
                        # ]
                        # ],
                        ]]
                        # Ticketrequestforme
                        #[setitem(g(),"ticketrequestforme_x",self),[MenuItem("TicketRequestForMe"), [MenuItem("+",callback=lambda _=None:[TicketRequestForMe(request=OSA.display_dialog("request?")).save(),self.set_menu()] )]+[eval("""[exec("from rumps import MenuItem",globals()),[MenuItem("%s"),MenuItem('''%s''', callback=lambda _=None: [Update(Get(TicketRequestForMe,request="%s"),response=OSA.display_dialog("response?: ")),g()["ticketrequestforme_x"].set_menu()]  )] ][1]""" % ( i.request,i.response,i.request,   )) for i in All(TicketRequestForMe)]]][1],

                        #THESE ARE ALL HOTFIXES, CANNOT USE THESE AS EXAMPLES.
                        #setitem(g(),"Scoresheet",ExecutableText().export("Scoresheet"))
                        # do not tuch.

                        #Ad
                        #Order
                        #Product
                      ]
      #@lolgoodedOSA().notify("Set Menulet.")
      # process(lambda: [[time.sleep(5),[Activity().stop([i for i in All(Activity) if(i.intervals not in [None,[]] and 1==len(i.intervals[-1]))][0].name), Activity().start("None") ] if("None"==OSA().display_dialog(["None","Continue"])) else None] for i in range(random.randrange(1000,2000))])
    def emails_in_menulet_as_png(self):
      """
      In [1]: for i in e.messages:                           
         ...:     t = i["hidden_message_3"].decode()
         ...:     try:
         ...:         address=html_to_png(t)
         ...:         impreview(address)
         ...:     except Exception as e:
         ...:         redprint(e)
      """
      return None
    def start(self):
      ""
  class Product_Handles:
    # Basically, it shows the day's sales for all shops, as well and if clicked, shows the adsets.
    def __init__(self):
      import rumps
      from rumps import MenuItem as M
      from rumps import MenuItem
      self.app = rumps.App("Product_Handles",quit_button=Null)
      globals().update(locals())


      self.set_menu()
      #process(  lambda: [time.sleep(6.15), self.set_menu()]  )
      time.sleep(4)
      self.app.run()


    def set_menu(self):
      keys = list(self.app.menu.keys())
      redprint(keys)
      for i in keys:
        self.app.menu.pop(i)
      keycall("Icon",All(Adset))
      self.app.menu = [MenuItem("/",callback=lambda _=None:[])]+[
                        MenuItem("") for i in All(Handle)
                      ]
  class Ryle:
    def __init__(self):
      import rumps
      from rumps import MenuItem as M
      from rumps import MenuItem
      self.app = rumps.App("🍃", quit_button=Null)
      globals().update(locals())


      self.set_menu()
      time.sleep(0)
      self.app.run()

    def set_menu(self):
      keys = list(self.app.menu.keys())
      redprint(keys)
      for i in keys:
        self.app.menu.pop(i)
      globals()["ryle"] = self
      self.app.title = "Setup"
      def helper(func,folder_name=None):
        L=multiprocessing_process(lambda:[[OSA.notify("%s, Running"%(str(datetime.now())),x=False),sp(1)] for i in range(WHILE_TRUE)])
        try:
          func()
          L.terminate()
          OSA.notify("%s: SUCCESS"%(datetime.now()))
        except Exception as e:
          L.terminate()
          OSA.notify("%s: ERROR"%(datetime.now()))
          OSA.log("Sorry, this part of setup has broken down due to lack of testing or a change in the website) this is a list of the urls and a folder with the screenshots and any shop information to update. please go thtrough them yourself to cotinue the setup.",tp=False)
          tryprocess(lambda:impreview(folder_name))
      get_cards = lambda: oset(listminus(flatten(keymulti(["AliExpress_Financial_Card_Information","GSuite_Financial_Card_Information","Shopify_Financial_Card_Information","Facebook_Financial_Card_Information",], All(Shop)),1),[None]))
      self.app.menu = [
      M("+", callback=lambda _=None: [Save(Shop,shop_abbreviation=OSA.display_dialog("Shop abbreviation [for example: qwe]?",default_answer=""),Fields_To_Update=[],Street_Address_Line_2=""),globals()["ryle"].set_menu()])] + [
      [i.shop_abbreviation,
      # [[M("Methods"),
      # eval("""[
      # M("Important Notifications", callback=lambda _=None:OSA.log("Notifications:\\n1. This will turn off Auto Update for Google Chrome.\\n2. Only Metric system is supported (kg).\\n3. Products not created through the product creater (so it will be in the files) will not be saved or managed.\\n4. The only type of 2fa supported is text message.\\n5. The street address will appear on https://<Administrative_Url>.myshopify.com/pages/privacy-policy\\n6. There was some intermediate pages which require completion of an account signup so these pages can\'t be tested daily. For example: To continually test the G Suite account creation flow daily would require numerous phone numbers per week. To test the purchasing of a domain name would require an actual domain name purchase every time, which is not possible.\\n7. Orders with note will be skipped and must be manually fulfilled.\\n8. Mac OS permission buttons and captchas and verification codes will have to be entered manually in the setup.\\n9. This program will not save products not created within the program. This program will also not order items in the orders for products not created within the program.\\n10. The time zone is set to EST, so between 12AM to 5:59:59AM (EST), any adset will begin at 6AM (EST) the same day. any other hours, it will begin the next day at 6AM (EST).\\n11. This will add products, order orders, update and display emails, and create ads. There should be a limited number of errors solved. Therefore, a csv file is supplied with each set of items in regards to the business and it should be read, and checks be made so that another party is making sure things are aligning properly. These files can be gotten from 'Run Exports'\\n12. You do not have to manage your finances with this.\\n13. Routing helps to keep track of the order status after the sale including time of sale, time order placed to AliExpress supplier, time tracking was posted, time order arrived to the customer. You don\'t need to use routing. You can get the tracking number inside your AliExpress account\'s order page.\\n14. Country codes that are not US will require manual address fill in during checkout\\n15. Only ePacket is supported for adding items and ordering items.\\n16. If you are on a prompt from the menulet and want to exit the prompt, use the hotkeys to reset everything and then answer the prompts with anything to exit the prompts.\\n")),
      # M("Get Gmail Account", callback=lambda _=None:helper(lambda:(Get(Shop,shop_abbreviation="%s").GET_GMAIL_ACCOUNT ()) )),
      # M("Get Shopify Store", callback=lambda _=None:helper(lambda:(Get(Shop,shop_abbreviation="%s").GET_SHOPIFY_STORE ()) )),
      # M("Get Shopify App", callback=lambda _=None:helper(lambda:(Get(Shop,shop_abbreviation="%s").GET_SHOPIFY_APP ()) )),
      # M("Get GSuite Account", callback=lambda _=None:helper(lambda:(Get(Shop,shop_abbreviation="%s").GET_GSUITE_ACCOUNT ()) )),
      # M("Get Google API Project - Gmail Account", callback=lambda _=None:helper(lambda:(Get(Shop,shop_abbreviation="%s").GET_GOOGLE_API_PROJECT ("%s") ))),
      # M("Get Google API Project - GSuite Account", callback=lambda _=None:helper(lambda:(Get(Shop,shop_abbreviation="%s").GET_GOOGLE_API_PROJECT ("%s") ))),
      # M("Get Facebook Account", callback=lambda _=None:helper(lambda:(Get(Shop,shop_abbreviation="%s").GET_FACEBOOK_ACCOUNT ()) )),
      # M("Get Facebook Business Manager Account", callback=lambda _=None:helper(lambda:(Get(Shop,shop_abbreviation="%s").GET_FACEBOOK_BUSINESS_MANAGER_ACCOUNT ()) )),
      # # call biz manager acc
      # M("Get Facebook Ad Account", callback=lambda _=None:helper(lambda:(Get(Shop,shop_abbreviation="%s").GET_FACEBOOK_AD_ACCOUNT ()) )),
      # M("Get Facebook Pixel", callback=lambda _=None:helper(lambda:(Get(Shop,shop_abbreviation="%s").GET_FACEBOOK_PIXEL ()) )),
      # # call get dev acc, always get acc/app
      # M("Get Facebook Developer Account", callback=lambda _=None:helper(lambda:(Get(Shop,shop_abbreviation="%s").GET_FACEBOOK_DEVELOPER_ACCOUNT ()) )),
      # M("Get Facebook Api", callback=lambda _=None:helper(lambda:(Get(Shop,shop_abbreviation="%s").GET_FACEBOOK_MARKETING_APP_IF_HAVE_DEVELOPER_ACCOUNT ()) )),
      # M("Get AliExpress Account", callback=lambda _=None:helper(lambda:(Get(Shop,shop_abbreviation="%s").GET_ALIEXPRESS_ACCOUNT ()) )),
      # M("Get AliPay Account", callback=lambda _=None:helper(lambda:(Get(Shop,shop_abbreviation="%s").GET_ALIPAY_ACCOUNT ()) )),
      # M("Run Rest Of Setup", callback=lambda _=None: OSA.log("At the end, select site payment plan, disable password page, pick a website theme, and edit the website menu, and choose your payment gateways. (\\n1. https://<Administrative_Url>.myshopify.com/admin/settings/account/plan \\n2. https://<Administrative_Url>.myshopify.com/admin/online_store/preferences, \\n3. https://<Administrative_Url>.myshopify.com/admin/themes, \\n4. https://<Administrative_Url>.myshopify.com/admin/menus, \\n5. https://<Administrative_Url>.myshopify.com/admin/settings/payments)") ),
      # ]"""%(i.shop_abbreviation, i.shop_abbreviation, i.shop_abbreviation, i.shop_abbreviation, i.shop_abbreviation, i.Gmail_Email_Address, i.shop_abbreviation, i.Business_Email_Address, i.shop_abbreviation, i.shop_abbreviation, i.shop_abbreviation, i.shop_abbreviation, i.shop_abbreviation, i.shop_abbreviation, i.shop_abbreviation, i.shop_abbreviation))
      # ]] + \
      # eval("""[[M("Has_Gmail_Account"), [(True)if(Get(Shop, shop_abbreviation="%s").Has_Gmail_Account)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Has_Gmail_Account=(True)if(OSA.display_dialog("Do you have a Gmail account?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Has_Shopify_Store"), [(True)if(Get(Shop, shop_abbreviation="%s").Has_Shopify_Store)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Has_Shopify_Store=(True)if(OSA.display_dialog("Do you have a Shopify Store?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Has_Namecheap_Account"), [(True)if(Get(Shop, shop_abbreviation="%s").Has_Namecheap_Account)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Has_Namecheap_Account=(True)if(OSA.display_dialog("Do you have a Namecheap Account?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Has_GSuite_Account"), [(True)if(Get(Shop, shop_abbreviation="%s").Has_GSuite_Account)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Has_GSuite_Account=(True)if(OSA.display_dialog("Do you have a GSuite Account?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Has_Facebook_Account"), [(True)if(Get(Shop, shop_abbreviation="%s").Has_Facebook_Account)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Has_Facebook_Account=(True)if(OSA.display_dialog("Do you have a Facebook Account?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Has_Facebook_Business_Manager_Account"), [(True)if(Get(Shop, shop_abbreviation="%s").Has_Facebook_Business_Manager_Account)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Has_Facebook_Business_Manager_Account=(True)if(OSA.display_dialog("Do you have a Facebook Business Manager Account?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Has_Facebook_Ad_Account_ID"), [(True)if(Get(Shop, shop_abbreviation="%s").Has_Facebook_Ad_Account_ID)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Has_Facebook_Ad_Account_ID=(True)if(OSA.display_dialog("Do you have a Facebook Ad Account?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Has_Facebook_Pixel"), [(True)if(Get(Shop, shop_abbreviation="%s").Has_Facebook_Pixel)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Has_Facebook_Pixel=(True)if(OSA.display_dialog("Do you have a Facebook Ad Account Pixel?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Has_Facebook_Developer_Account"), [(True)if(Get(Shop, shop_abbreviation="%s").Has_Facebook_Developer_Account)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Has_Facebook_Developer_Account=(True)if(OSA.display_dialog("Do you have a Facebook Developer Account?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Has_AliExpress_Account"), [(True)if(Get(Shop, shop_abbreviation="%s").Has_AliExpress_Account)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Has_AliExpress_Account=(True)if(OSA.display_dialog("Do you have an AliExpress Account?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Gmail_Email_Address"), [(Get(Shop, shop_abbreviation="%s").Gmail_Email_Address), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Gmail_Email_Address=(OSA.display_dialog("Gmail email address?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Gmail_Password"), [("".join(["•" for i in rangelen(Get(Shop, shop_abbreviation="%s").Gmail_Password)]))if(Get(Shop,shop_abbreviation="%s").Gmail_Password)else(None), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Gmail_Password=(OSA.display_dialog('Gmail password [note: As per https://support.google.com/accounts/answer/32040?hl=en, the accepted characters are: "any combination of letters, numbers, and symbols (ASCII characters)". There may be more rules such as repeating letters, etc that prevent certain passwords.]?',default_answer="",hidden=True))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Number_To_Receive_Videocalls_And_Messages"), [(True)if(Get(Shop, shop_abbreviation="%s").Number_To_Receive_Videocalls_And_Messages)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Number_To_Receive_Videocalls_And_Messages=(True)if(OSA.display_dialog("Do you want to use this phone number to receive video calls and messages with this Gmail account?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Business_Name"), [(Get(Shop, shop_abbreviation="%s").Business_Name), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Business_Name=(OSA.display_dialog("Business Name?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Employee_Count"), [(Get(Shop, shop_abbreviation="%s").Employee_Count), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Employee_Count=(OSA.display_dialog("How many employees are in this company [Has To Be Greater Than 0]?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Country_Of_Business"), [(Get(Shop, shop_abbreviation="%s").Country_Of_Business), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Country_Of_Business=(OSA.display_dialog("Country Of Business [Only United States is supported currently. Put United States as your answer. Make sure to capitalize correctly.]?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("First_Name"), [(Get(Shop, shop_abbreviation="%s").First_Name), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),First_Name=(OSA.display_dialog("First name?",default_answer="").title())),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Last_Name"), [(Get(Shop, shop_abbreviation="%s").Last_Name), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Last_Name=(OSA.display_dialog("Last name?",default_answer="").title())),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Street_Address"), [(Get(Shop, shop_abbreviation="%s").Street_Address), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Street_Address=(OSA.display_dialog("Street address?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Street_Address_Line_2"), [(Get(Shop, shop_abbreviation="%s").Street_Address_Line_2), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Street_Address_Line_2=(OSA.display_dialog("Street address line 2 [Enter in nothing if empty]?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("State"), [(Get(Shop, shop_abbreviation="%s").State), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),State=(OSA.display_dialog("State? [Enter in the state abbreviation]",default_answer="").upper())),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("City"), [(Get(Shop, shop_abbreviation="%s").City), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),City=(OSA.display_dialog("City?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("ZIP_Code"), [(Get(Shop, shop_abbreviation="%s").ZIP_Code), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),ZIP_Code=(OSA.display_dialog("Zip code?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Business_Phone_Number"), [(Get(Shop, shop_abbreviation="%s").Business_Phone_Number), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Business_Phone_Number=(Integer(OSA.display_dialog("Business phone number?",default_answer="")))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Business_Email_Address"), [(Get(Shop, shop_abbreviation="%s").Business_Email_Address), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Business_Email_Address=(OSA.display_dialog("Business email address [note: this will be your GSuite Account username. The business email address can be <Business Email Address>@<Domain Name>.com, for example: support@mystorename.com, or sales@mystorename.com.]?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("GSuite_Password"), [("".join(["•" for i in rangelen(Get(Shop, shop_abbreviation="%s").GSuite_Password)]))if(Get(Shop,shop_abbreviation="%s").GSuite_Password)else(None), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),GSuite_Password=(OSA.display_dialog('GSuite password [note: As per https://support.google.com/accounts/answer/32040?hl=en, the accepted characters are: "any combination of letters, numbers, and symbols (ASCII characters)". There may be more rules such as repeating letters, etc that prevent certain passwords.]?',default_answer="",hidden=True))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Product_Return_Address"), [(Get(Shop, shop_abbreviation="%s").Product_Return_Address), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Product_Return_Address=(OSA.display_dialog("Product Return Address [for example: 111 Xyz Street, Anytown, AB 36016, United States]?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Shopify_Email"), [(Get(Shop, shop_abbreviation="%s").Shopify_Email), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Shopify_Email=(OSA.display_dialog("Shopify email [note: if you are creating a Shopify store, input your Gmail email address.]?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Shopify_Password"), [("".join(["•" for i in rangelen(Get(Shop, shop_abbreviation="%s").Shopify_Password)]))if(Get(Shop,shop_abbreviation="%s").Shopify_Password)else(None), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Shopify_Password=(OSA.display_dialog("Shopify password [note: accepted characters include all punctuation marks, letters, and numbers. There may be more rules such as repeating letters, etc that prevent certain passwords.]?",default_answer="",hidden=True))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Administrative_Url"), [M("Help", callback=lambda _=None:OSA.display_dialog("Shopify administrative url [note: this is the url to log into the shop. It will be in the format of https://<Personal Store URL>.myshopify.com/admin. Please only enter in letters, numbers, and dashes. For example: https://mystorename.myshopify.com/admin.]?",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").Administrative_Url), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Administrative_Url=(OSA.display_dialog("Shopify administrative url [note: this is the url to log into the shop. It will be in the format of https://<Administrative Url>.myshopify.com/admin. Please only enter in letters, numbers, and dashes. For example: https://mystorename.myshopify.com/admin.]?",default_answer=""))),OSA.display_dialog("This url is taken. If this url does not belong to you, please input a new administrative url.",text_prompt=False)if(("https://app.shopify.com/services/login/identity")in(requests.get(Get(Shop,shop_abbreviation="%s").Administrative_Url).text))else(),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \

      #eval("""[[M("Homepage_Title [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("Homepage title [For Search Engine Optimization]?",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").Homepage_Title), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Homepage_Title=(OSA.display_dialog("Homepage title [For Search Engine Optimization]?",default_answer="")),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Homepage_Title"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Homepage_Meta_Description [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("Homepage meta description [For Search Engine Optimization]?",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").Homepage_Meta_Description), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Homepage_Meta_Description=(OSA.display_dialog("Homepage meta description [For Search Engine Optimization]?")),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Homepage_Meta_Description"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Metric_System [Has to be Metric system. Imperial system is not supported as of now.]"), [M("Help", callback=lambda _=None:OSA.display_dialog("Metric system [Only Metric system is supported (kg)]?",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").Metric_System), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Metric_System=(OSA.display_dialog("Metric system [Only Metric system is supported (kg)]?",default_answer="").capitalize()),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Metric_System"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Facebook_Pixel_ID"), [M("Help", callback=lambda _=None:OSA.display_dialog("Facebook pixel id?",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").Facebook_Pixel_ID), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Facebook_Pixel_ID=(Integer(OSA.display_dialog("Facebook pixel id?",default_answer=""))),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Facebook_Pixel_ID"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Checkout_With_Account [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("Should the customer check out with a store account [options are: disabled, optional, required]?",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").Checkout_With_Account), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Checkout_With_Account=(OSA.display_dialog("Should the customer check out with a store account [options are: disabled, optional, required]?",default_answer="")),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Checkout_With_Account"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Checkout_With_Identifier [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("What contact information should the customer check out with [options are: phone_or_email, email]?",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").Checkout_With_Identifier), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Checkout_With_Identifier=(OSA.display_dialog("What contact information should the customer check out with [options are: phone_or_email, email]?",default_answer="")),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Checkout_With_Identifier"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Receive_Shipping_Updates [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("Send the customer shipping updates after their order?",text_prompt=False)), (False)if(Get(Shop, shop_abbreviation="%s").Receive_Shipping_Updates==False)else(True), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Receive_Shipping_Updates=((True)if(OSA.display_dialog("Send the customer shipping updates after their order?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Receive_Shipping_Updates"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Checkout_With_Name [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("During checkout, require the customer to enter in their full name or last name only [options are: require_last_only, require_first_and_last]?",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").Checkout_With_Name), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Checkout_With_Name=(OSA.display_dialog("During checkout, require the customer to enter in their full name or last name only [options are: require_last_only, require_first_and_last]?",default_answer="")),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Checkout_With_Name"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Checkout_With_Company [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("During checkout, should the customer be prompted for the company in their shipping and billing address [options are: hidden, optional, required]?",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").Checkout_With_Company), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Checkout_With_Company=(OSA.display_dialog("During checkout, should the customer be prompted for the company in their shipping and billing address [options are: hidden, optional, required]?",default_answer="")),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Checkout_With_Company"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Checkout_With_Address_Line_2 [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("During checkout, should the customer be prompted for the shipping address line 2 in their shipping and billing address [options are: hidden, optional, required]?",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").Checkout_With_Address_Line_2), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Checkout_With_Address_Line_2=(OSA.display_dialog("During checkout, should the customer be prompted for the shipping address line 2 in their shipping and billing address [options are: hidden, optional, required]?",default_answer="")),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Checkout_With_Address_Line_2"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Checkout_With_Phone_Number [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("During checkout, should the customer be prompted for their phone number in their shipping and billing information [options are: hidden, optional, required]?",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").Checkout_With_Phone_Number), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Checkout_With_Phone_Number=(OSA.display_dialog("During checkout, should the customer be prompted for their phone number in their shipping and billing information [options are: hidden, optional, required]?",default_answer="")),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Checkout_With_Phone_Number"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Checkout_With_Shipping_As_Billing [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("During checkout, should the billing address for the customer's payment information be the shipping address by default?",text_prompt=False)), (False)if(Get(Shop, shop_abbreviation="%s").Checkout_With_Shipping_As_Billing==False)else(True), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Checkout_With_Shipping_As_Billing=((True)if(OSA.display_dialog("During checkout, should the billing address for the customer's payment information be the shipping address by default?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Checkout_With_Shipping_As_Billing"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Checkout_Enable_Address_Autocomplete [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("During checkout, enable address autocompletion?",text_prompt=False)), (True)if(Get(Shop, shop_abbreviation="%s").Checkout_Enable_Address_Autocomplete)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Checkout_Enable_Address_Autocomplete=((True)if(OSA.display_dialog("During checkout, enable address autocompletion?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Checkout_Enable_Address_Autocomplete"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Show_Email_Signup_Option_At_Checkout [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("Show email signup option at checkout?",text_prompt=False)), (True)if(Get(Shop, shop_abbreviation="%s").Show_Email_Signup_Option_At_Checkout)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Show_Email_Signup_Option_At_Checkout=((True)if(OSA.display_dialog("Show email signup option at checkout?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Show_Email_Signup_Option_At_Checkout"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Preselect_Email_Signup_Option_At_Checkout [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("Preselct the email signup option at checkout [This only applies if Show email signup option at checkout is on]?",text_prompt=False)), (True)if(Get(Shop, shop_abbreviation="%s").Preselect_Email_Signup_Option_At_Checkout)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Preselect_Email_Signup_Option_At_Checkout=((True)if(OSA.display_dialog("Preselct the email signup option at checkout [This only applies if Show email signup option at checkout is on]?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Preselect_Email_Signup_Option_At_Checkout"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Use_Free_Plus_Shipping [Fill this out if you plan on using Free + Ship]"), [M("Help", callback=lambda _=None:OSA.display_dialog("Use free plus shipping rates in your store [Set this to yes if you plan on using free plus shipping to price products. This only applies to products sold in AliExpress for under $9.95, so on the store, the product will be priced at $0 and the shipping will be $9.95]?",text_prompt=False)), (True)if(Get(Shop, shop_abbreviation="%s").Use_Free_Plus_Shipping)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Use_Free_Plus_Shipping=((True)if(OSA.display_dialog("Use free plus shipping rates in your store [Set this to yes if you plan on using free plus shipping to price products. This only applies to products sold in AliExpress for under $9.95, so on the store, the product will be priced at $0 and the shipping will be $9.95]?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Use_Free_Plus_Shipping"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      
      ## eval("""[[M("Shopify_App_API_Key"), [M("Help", callback=lambda _=None:OSA.display_dialog("Shopify app API password?",text_prompt=False)), ("".join(["•" for i in rangelen(Get(Shop, shop_abbreviation="%s").Shopify_App_API_Key)]))if(Get(Shop,shop_abbreviation="%s").Shopify_App_API_Key)else(None), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Shopify_App_API_Key=(OSA.display_dialog("Shopify app API password?",default_answer="",hidden=True))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Shopify_App_API_Password"), [M("Help", callback=lambda _=None:OSA.display_dialog("Shopify app API key?",text_prompt=False)), ("".join(["•" for i in rangelen(Get(Shop, shop_abbreviation="%s").Shopify_App_API_Password)]))if(Get(Shop,shop_abbreviation="%s").Shopify_App_API_Password)else(None), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Shopify_App_API_Password=(OSA.display_dialog("Shopify app API key?",default_answer="",hidden=True))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Shopify_App_API_Secret"), [M("Help", callback=lambda _=None:OSA.display_dialog("Shopify app API secret?",text_prompt=False)), ("".join(["•" for i in rangelen(Get(Shop, shop_abbreviation="%s").Shopify_App_API_Secret)]))if(Get(Shop,shop_abbreviation="%s").Shopify_App_API_Secret)else(None), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Shopify_App_API_Secret=(OSA.display_dialog("Shopify app API secret?",default_answer="",hidden=True))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Shopify_App_API_Url"), [M("Help", callback=lambda _=None:OSA.display_dialog("Shopify App API Url [for example: https://<Shopify App API Key>:<Shopify App API Password>@<Shopify Admin URL>/admin]?",text_prompt=False)), ("".join(["•" for i in rangelen(Get(Shop, shop_abbreviation="%s").Shopify_App_API_Url)]))if(Get(Shop,shop_abbreviation="%s").Shopify_App_API_Url)else(None), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Shopify_App_API_Url=(OSA.display_dialog("Shopify App API Url [for example: https://<Shopify App API Key>:<Shopify App API Password>@<Shopify Admin URL>/admin]?",default_answer="",hidden=True))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Pages [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("Create The Default Pages [This will create the Terms Of Service, Privacy Policy, Refund Policy, DMCA, and Contact Us pages]?",text_prompt=False)), (True)if(Get(Shop, shop_abbreviation="%s").Pages)else(False), M("Update", callback=lambda _=None:([Update(Get(Shop,shop_abbreviation="%s"),Pages=True,Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Pages"])])if(OSA.display_dialog("Create The Default Pages [This will create the Terms Of Service, Privacy Policy, Refund Policy, DMCA, and Contact Us pages]?",text_prompt=False,buttons=["Yes","No"])=="Yes")else())]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Default_Product_Description"), [M("Help", callback=lambda _=None:OSA.display_dialog("Default Product Description in HTML with potential size chart insert as <Size Chart> and potential unique description insert as <Unique Description> and potential unique description insert as <Unique Description> [note: For an HTML editor, visit https://your-shop-name.myshopify.com/admin/pages/new (substitute your-shop-name with your shop's myshopify url) and click the Show HTML button which is above the top right of the text box, or visit: https://html-online.com/editor/. As well, note that if <Size Chart> is included, each time a product is added, if a size chart is specified along with it, the size chart will take the place of <Size Chart>. If <Unique Description> is included, each time a product is added, if a unique product description is specified along with it, the unique product description will take the place of <Unique Description>]?",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").Default_Product_Description), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Default_Product_Description=(OSA.display_dialog("Default Product Description in HTML with potential size chart insert as <Size Chart> and potential unique description insert as <Unique Description> [note: For an HTML editor, visit https://your-shop-name.myshopify.com/admin/pages/new (substitute your-shop-name with your shop's myshopify url) and click the Show HTML button which is above the top right of the text box, or visit: https://html-online.com/editor/. As well, note that if <Size Chart> is included, each time a product is added, if a size chart is specified along with it, the size chart will take the place of <Size Chart>. If <Unique Description> is included, each time a product is added, if a unique product description is specified along with it, the unique product description will take the place of <Unique Description>.]?",default_answer="\\n"*60))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Domain_Name_To_Transfer [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("Do you already own a domain name to transfer to this shop?",text_prompt=False)), (True)if(Get(Shop, shop_abbreviation="%s").Domain_Name_To_Transfer)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Domain_Name_To_Transfer=(True)if(OSA.display_dialog("Do you already own a domain name to transfer to this shop?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Domain_Name"), [M("Help", callback=lambda _=None:OSA.display_dialog("Domain name [for example: domain-name.com. As of now numbers are not supported in the domain name.]?",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").Domain_Name), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Domain_Name=OSA.display_dialog("Domain name [for example: domain-name.com]?",default_answer=""),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Domain_Name"]),check_domain_name_via_shopify(Get(Shop,shop_abbreviation="%s").Domain_Name),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Renew_Domain_Every_Year [**Fill this out if you have to create a shop]"), [M("Help", callback=lambda _=None:OSA.display_dialog("Do you want to renew the domain name every year [this applies if you are purchasing the domain name]?",text_prompt=False)), (True)if(Get(Shop, shop_abbreviation="%s").Renew_Domain_Every_Year)else(False), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Renew_Domain_Every_Year=(True)if(OSA.display_dialog("Do you want to renew the domain name every year [this applies if you are purchasing the domain name]?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Facebook_Email"), [(Get(Shop, shop_abbreviation="%s").Facebook_Email), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Facebook_Email=(OSA.display_dialog("Facebook email?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("Facebook_Password"), [("".join(["•" for i in rangelen(Get(Shop, shop_abbreviation="%s").Facebook_Password)]))if(Get(Shop,shop_abbreviation="%s").Facebook_Password)else(None), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Facebook_Password=(OSA.display_dialog("Facebook password [note: accepted characters include all punctuation marks, letters, and numbers. There may be more rules such as repeating letters, etc that prevent certain passwords.]?",default_answer="",hidden=True))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Date_Of_Birth"), [(Get(Shop, shop_abbreviation="%s").Date_Of_Birth), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Date_Of_Birth=(Integer(OSA.display_dialog("Date of birth [for example: 01011990]?",default_answer="")))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Gender"), [(Get(Shop, shop_abbreviation="%s").Gender), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Gender=(OSA.display_dialog("Gender [options are: female, male]?",default_answer="").lower())),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Facebook_Business_Account_Business_Name"), [(Get(Shop, shop_abbreviation="%s").Facebook_Business_Account_Business_Name), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Facebook_Business_Account_Business_Name=(OSA.display_dialog("Facebook business account name [only letters and numbers are allowed here.]?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Facebook_Business_Manager_ID"), [(Get(Shop, shop_abbreviation="%s").Facebook_Business_Manager_ID), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Facebook_Business_Manager_ID=(Integer(OSA.display_dialog("Facebook business manager ID?",default_answer="")))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Facebook_Business_Ad_Account_Name"), [(Get(Shop, shop_abbreviation="%s").Facebook_Business_Ad_Account_Name), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Facebook_Business_Ad_Account_Name=(OSA.display_dialog("Facebook business ad account name?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Facebook_Business_Ad_Account_Time_Zone"), [(Get(Shop, shop_abbreviation="%s").Facebook_Business_Ad_Account_Time_Zone), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Facebook_Business_Ad_Account_Time_Zone=(OSA.display_dialog("Facebook business ad account time zone?",dropdown_options=["(GMT-10:00) Pacific/Honolulu","(GMT-09:00) America/Anchorage","(GMT-08:00) America/Dawson","(GMT-08:00) America/Los Angeles","(GMT-08:00) America/Tijuana","(GMT-08:00) America/Vancouver","(GMT-07:00) America/Dawson Creek","(GMT-07:00) America/Denver","(GMT-07:00) America/Edmonton","(GMT-07:00) America/Hermosillo","(GMT-07:00) America/Mazatlan","(GMT-07:00) America/Phoenix","(GMT-06:00) Africa/Abidjan","(GMT-06:00) America/Chicago","(GMT-06:00) America/Costa Rica","(GMT-06:00) America/El Salvador","(GMT-06:00) America/Guatemala","(GMT-06:00) America/Managua","(GMT-06:00) America/Mexico City","(GMT-06:00) America/Rainy River","(GMT-06:00) America/Regina","(GMT-06:00) America/Tegucigalpa","(GMT-06:00) Pacific/Galapagos","(GMT-05:00) Africa/Addis Ababa","(GMT-05:00) America/Atikokan","(GMT-05:00) America/Bogota","(GMT-05:00) America/Guayaquil","(GMT-05:00) America/Iqaluit","(GMT-05:00) America/Jamaica","(GMT-05:00) America/Lima","(GMT-05:00) America/Nassau","(GMT-05:00) America/New York","(GMT-05:00) America/Panama","(GMT-05:00) America/Toronto","(GMT-05:00) Pacific/Easter","(GMT-04:00) America/Blanc-Sablon","(GMT-04:00) America/Campo Grande","(GMT-04:00) America/Caracas","(GMT-04:00) America/Halifax","(GMT-04:00) America/La Paz","(GMT-04:00) America/Port of_Spain","(GMT-04:00) America/Puerto Rico","(GMT-04:00) America/Santo Domingo","(GMT-03:30) America/St Johns","(GMT-03:00) America/Argentina/Buenos Aires","(GMT-03:00) America/Argentina/Salta","(GMT-03:00) America/Argentina/San Luis","(GMT-03:00) America/Asuncion","(GMT-03:00) America/Belem","(GMT-03:00) America/Montevideo","(GMT-03:00) America/Santiago","(GMT-03:00) America/Sao Paulo","(GMT-02:00) America/Noronha","(GMT-01:00) Atlantic/Azores","(GMT+00:00) Africa/Accra","(GMT+00:00) Africa/Casablanca","(GMT+00:00) Atlantic/Canary","(GMT+00:00) Atlantic/Reykjavik","(GMT+00:00) Europe/Dublin","(GMT+00:00) Europe/Lisbon","(GMT+00:00) Europe/London","(GMT+01:00) Africa/Lagos","(GMT+01:00) Africa/Tunis","(GMT+01:00) Europe/Amsterdam","(GMT+01:00) Europe/Belgrade","(GMT+01:00) Europe/Berlin","(GMT+01:00) Europe/Bratislava","(GMT+01:00) Europe/Brussels","(GMT+01:00) Europe/Budapest","(GMT+01:00) Europe/Copenhagen","(GMT+01:00) Europe/Ljubljana","(GMT+01:00) Europe/Luxembourg","(GMT+01:00) Europe/Madrid","(GMT+01:00) Europe/Malta","(GMT+01:00) Europe/Oslo","(GMT+01:00) Europe/Paris","(GMT+01:00) Europe/Prague","(GMT+01:00) Europe/Rome","(GMT+01:00) Europe/Sarajevo","(GMT+01:00) Europe/Skopje","(GMT+01:00) Europe/Stockholm","(GMT+01:00) Europe/Vienna","(GMT+01:00) Europe/Warsaw","(GMT+01:00) Europe/Zagreb","(GMT+01:00) Europe/Zurich","(GMT+02:00) Africa/Cairo","(GMT+02:00) Africa/Johannesburg","(GMT+02:00) Asia/Amman","(GMT+02:00) Asia/Beirut","(GMT+02:00) Asia/Gaza","(GMT+02:00) Asia/Jerusalem","(GMT+02:00) Asia/Nicosia","(GMT+02:00) Europe/Athens","(GMT+02:00) Europe/Bucharest","(GMT+02:00) Europe/Helsinki","(GMT+02:00) Europe/Kaliningrad","(GMT+02:00) Europe/Kiev","(GMT+02:00) Europe/Riga","(GMT+02:00) Europe/Sofia","(GMT+02:00) Europe/Tallinn","(GMT+02:00) Europe/Vilnius","(GMT+03:00) Africa/Nairobi","(GMT+03:00) Asia/Baghdad","(GMT+03:00) Asia/Bahrain","(GMT+03:00) Asia/Kuwait","(GMT+03:00) Asia/Qatar","(GMT+03:00) Asia/Riyadh","(GMT+03:00) Europe/Istanbul","(GMT+03:00) Europe/Moscow","(GMT+04:00) Asia/Dubai","(GMT+04:00) Asia/Muscat","(GMT+04:00) Europe/Samara","(GMT+04:00) Indian/Mauritius","(GMT+05:00) Asia/Karachi","(GMT+05:00) Asia/Yekaterinburg","(GMT+05:00) Indian/Maldives","(GMT+05:30) Asia/Colombo","(GMT+05:30) Asia/Kolkata","(GMT+05:45) Africa/Asmara","(GMT+06:00) Asia/Dhaka","(GMT+06:00) Asia/Omsk","(GMT+07:00) Asia/Bangkok","(GMT+07:00) Asia/Ho Chi_Minh","(GMT+07:00) Asia/Jakarta","(GMT+07:00) Asia/Krasnoyarsk","(GMT+08:00) Asia/Hong Kong","(GMT+08:00) Asia/Irkutsk","(GMT+08:00) Asia/Kuala Lumpur","(GMT+08:00) Asia/Makassar","(GMT+08:00) Asia/Manila","(GMT+08:00) Asia/Shanghai","(GMT+08:00) Asia/Singapore","(GMT+08:00) Asia/Taipei","(GMT+08:00) Australia/Perth","(GMT+09:00) Asia/Jayapura","(GMT+09:00) Asia/Seoul","(GMT+09:00) Asia/Tokyo","(GMT+09:00) Asia/Yakutsk","(GMT+10:00) Asia/Vladivostok","(GMT+10:30) Australia/Broken Hill","(GMT+11:00) Africa/Algiers","(GMT+11:00) Asia/Magadan","(GMT+11:00) Australia/Sydney","(GMT+12:00) Asia/Kamchatka","(GMT+13:00) Pacific/Auckland"]))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Facebook_Business_Ad_Account_ID"), [(Get(Shop, shop_abbreviation="%s").Facebook_Business_Ad_Account_ID), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Facebook_Business_Ad_Account_ID=(Integer(OSA.display_dialog("Facebook business ad account ID?",default_answer="")))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Facebook_Business_App_Secret"), [("".join(["•" for i in rangelen(Get(Shop, shop_abbreviation="%s").Facebook_Business_App_Secret)]))if(Get(Shop,shop_abbreviation="%s").Facebook_Business_App_Secret)else(None), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Facebook_Business_App_Secret=(OSA.display_dialog("Facebook business app secret?",default_answer="",hidden=True))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("Facebook_Business_App_Token"), [("".join(["•" for i in rangelen(Get(Shop, shop_abbreviation="%s").Facebook_Business_App_Token)]))if(Get(Shop,shop_abbreviation="%s").Facebook_Business_App_Token)else(None), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Facebook_Business_App_Token=(OSA.display_dialog("Facebook business app token?",default_answer="",hidden=True))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("AliExpress_Email"), [(Get(Shop, shop_abbreviation="%s").AliExpress_Email), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),AliExpress_Email=(OSA.display_dialog("AliExpress email?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      ## eval("""[[M("AliExpress_Password"), [("".join(["•" for i in rangelen(Get(Shop, shop_abbreviation="%s").AliExpress_Password)]))if(Get(Shop,shop_abbreviation="%s").AliExpress_Password)else(None), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),AliExpress_Password=(OSA.display_dialog("AliExpress password [only letters and numbers are allowed in this password, and the password length has to be between 6 and 20.]?",default_answer="",hidden=True))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      eval("""[[M("AliExpress_Most_Recent_Date"), [M("Help", callback=lambda _=None:OSA.display_dialog("Aliexpress Most Recent Date is the most recent date for the orders that are for this shop. If there are AliExpress orders before this date, they will be ignored. If all orders for this shop and time frame are start from one week ago, enter in the date that is one week ago. For example: 01/01/2018",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").AliExpress_Most_Recent_Date), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),AliExpress_Most_Recent_Date=(datetime.strptime(OSA.display_dialog("Aliexpress Most Recent Date is the most recent date for the orders that are for this shop. If there are AliExpress orders before this date, they will be ignored. If all orders for this shop and time frame are start from one week ago, enter in the date that is one week ago. For example: 01/01/2018",default_answer="month/date/year"),"%%m/%%d/%%Y"))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("AliPay_Pin"), [("".join(["•" for i in rangelen(Get(Shop, shop_abbreviation="%s").AliPay_Pin)]))if(Get(Shop,shop_abbreviation="%s").AliPay_Pin)else(None), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),AliPay_Pin=(OSA.display_dialog("AliPay pin [note: please enter a six digit pin. for example: 123456]?",default_answer="",hidden=True))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("AliPay_Security_Question_1 [Fill this out if you have to create an account]"), [(("{}: {}".format((list(Get(Shop, shop_abbreviation="%s").AliPay_Security_Question_1.keys())[0]), (list(Get(Shop, shop_abbreviation="%s").AliPay_Security_Question_1.values())[0])))if(type(Get(Shop, shop_abbreviation="%s").AliPay_Security_Question_1)==dict)else(None)), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),AliPay_Security_Question_1={(OSA.display_dialog("Security Question 1 [note: please pick three unique security questions.]?",dropdown_options=["What is your favorite color?","In which city were you born?","What is the name of your first university?","What is your father's name?","What is your mother's name?","What is your favorite fruit?","Who was your childhood best friend?","What was the name of your first pet?","Who is your favorite author?","Who was your favorite teacher?","Who was your first roommate?","Who was your first boss?"])):(OSA.display_dialog("Answer to security question 1?",default_answer=""))}),(OSA.display_dialog("Security question 1 conflicts with another security question. Please choose a new security question.",text_prompt=False))if((list(Shop()("%s").AliPay_Security_Question_1.keys())[0]) in [or_list(tryreturn(lambda:list(Shop()("%s").AliPay_Security_Question_3.keys())[0]),([])),or_list(tryreturn(lambda:list(Shop()("%s").AliPay_Security_Question_2.keys())[0]),([]))])else(),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("AliPay_Security_Question_2 [Fill this out if you have to create an account]"), [(("{}: {}".format((list(Get(Shop, shop_abbreviation="%s").AliPay_Security_Question_2.keys())[0]), (list(Get(Shop, shop_abbreviation="%s").AliPay_Security_Question_2.values())[0])))if(type(Get(Shop, shop_abbreviation="%s").AliPay_Security_Question_2)==dict)else(None)), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),AliPay_Security_Question_2={(OSA.display_dialog("Security Question 2 [note: please pick three unique security questions.]?",dropdown_options=["What is your favorite color?","In which city were you born?","What is the name of your first university?","What is your father's name?","What is your mother's name?","What is your favorite fruit?","Who was your childhood best friend?","What was the name of your first pet?","Who is your favorite author?","Who was your favorite teacher?","Who was your first roommate?","Who was your first boss?"])):(OSA.display_dialog("Answer to security question 2?",default_answer=""))}),(OSA.display_dialog("Security question 2 conflicts with another security question. Please choose a new security question.",text_prompt=False))if((list(Shop()("%s").AliPay_Security_Question_2.keys())[0]) in [or_list(tryreturn(lambda:list(Shop()("%s").AliPay_Security_Question_3.keys())[0]),([])),or_list(tryreturn(lambda:list(Shop()("%s").AliPay_Security_Question_1.keys())[0]),([]))])else(),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      # eval("""[[M("AliPay_Security_Question_3 [Fill this out if you have to create an account]"), [(("{}: {}".format((list(Get(Shop, shop_abbreviation="%s").AliPay_Security_Question_3.keys())[0]), (list(Get(Shop, shop_abbreviation="%s").AliPay_Security_Question_3.values())[0])))if(type(Get(Shop, shop_abbreviation="%s").AliPay_Security_Question_3)==dict)else(None)), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),AliPay_Security_Question_3={(OSA.display_dialog("Security Question 3 [note: please pick three unique security questions.]?",dropdown_options=["What is your favorite color?","In which city were you born?","What is the name of your first university?","What is your father's name?","What is your mother's name?","What is your favorite fruit?","Who was your childhood best friend?","What was the name of your first pet?","Who is your favorite author?","Who was your favorite teacher?","Who was your first roommate?","Who was your first boss?"])):(OSA.display_dialog("Answer to security question 3?",default_answer=""))}),(OSA.display_dialog("Security question 3 conflicts with another security question. Please choose a new security question.",text_prompt=False))if((list(Shop()("%s").AliPay_Security_Question_3.keys())[0]) in [or_list(tryreturn(lambda:list(Shop()("%s").AliPay_Security_Question_2.keys())[0]),([])),or_list(tryreturn(lambda:list(Shop()("%s").AliPay_Security_Question_1.keys())[0]),([]))])else(),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \

      eval("""[[M("AliExpress_Card_Transaction_Tags"), [M("Help", callback=lambda _=None:OSA.display_dialog("AliExpress card transaction tags [For example: aliexpress, ali if the card transaction tags have aliexpress in the description (enter in the lower case form, separated by ', ')]?",text_prompt=False)), (str(Get(Shop, shop_abbreviation="%s").AliExpress_Card_Transaction_Tags)), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),AliExpress_Card_Transaction_Tags=(lmap(lambda i: i.lower(), OSA.display_dialog("AliExpress card transaction tags [For example: aliexpress, ali if the card transaction tags have aliexpress in the description (enter in the lower case form separated by ', ')]?").split(", ")))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      eval("""[[M("Adspend_Card_Transaction_Tags"), [M("Help", callback=lambda _=None:OSA.display_dialog("Facebook adspend card transaction tags [For example: facebook, fb if the card transaction tags have facebook in the description (enter in the lower case form separated by ', ')]?",text_prompt=False)), (str(Get(Shop, shop_abbreviation="%s").Adspend_Card_Transaction_Tags)), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Adspend_Card_Transaction_Tags=(lmap(lambda i: i.lower(), OSA.display_dialog("Facebook adspend card transaction tags [For example: facebook, fb if the card transaction tags have facebook in the description (enter in the lower case form, separated by ', ')]?").split(", ")))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      eval("""[[M("Payment_Gateway_Payout_Card_Transaction_Tags"), [M("Help", callback=lambda _=None:OSA.display_dialog("Payment gateway payout card transaction tags [For example: stripe if the card transaction tags have stripe in the description (enter in the lower case form separated by ', ')]?",text_prompt=False)), (str(Get(Shop, shop_abbreviation="%s").Payment_Gateway_Payout_Card_Transaction_Tags)), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Payment_Gateway_Payout_Card_Transaction_Tags=(lmap(lambda i: i.lower(), OSA.display_dialog("Payment gateway payout card transaction tags [For example: stripe if the card transaction tags have stripe in the description (enter in the lower case form separated by ', ')]?").split(", ")))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      eval("""[[M("Lineitem_Most_Recent_Date"), [M("Help", callback=lambda _=None:OSA.display_dialog("Lineitem most recent date for getting orders [for example 01/01/2018]?",text_prompt=False)), (Get(Shop, shop_abbreviation="%s").Lineitem_Most_Recent_Date), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Lineitem_Most_Recent_Date=(datetime.strptime(OSA.display_dialog("Lineitem most recent date for getting orders [for example 01/01/2018]?",default_answer="month/date/year"),"%%m/%%d/%%Y"))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \

      ## eval("""[[M("Allow_Additional_Shipping_Methods"), [M("Help", callback=lambda _=None:OSA.display_dialog("Allow additional shipping methods? This will allow adding products with more than just ePacket as a shipping method.",text_prompt=False)), (False)if(Get(Shop, shop_abbreviation="%s").Allow_Additional_Shipping_Methods==False)else(True), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Allow_Additional_Shipping_Methods=((True)if(OSA.display_dialog("Allow additional shipping methods? This will allow adding products with more than just ePacket as a shipping method.",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      eval("""[[M("Send_Tracking_Number"), [M("Help", callback=lambda _=None:OSA.display_dialog("Send tracking numbers? This will send the tracking number if gotten. Otherwise you can look up the tracking number if you have an email and then send it in the email.",text_prompt=False)), (False)if(Get(Shop, shop_abbreviation="%s").Send_Tracking_Number==False)else(True), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Send_Tracking_Number=((True)if(OSA.display_dialog("Send tracking numbers? This will send the tracking number if gotten. Otherwise you can look up the tracking number if you have an email and then send it in the email.",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \

      eval("""[[M("DBC_Username"), [(Get(Shop, shop_abbreviation="%s").DBC_Username), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),DBC_Username=(OSA.display_dialog("Death By Captcha username?",default_answer=""))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      eval("""[[M("DBC_Password"), [("".join(["•" for i in rangelen(Get(Shop, shop_abbreviation="%s").DBC_Password)]))if(Get(Shop,shop_abbreviation="%s").DBC_Password)else(None), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),DBC_Password=(OSA.display_dialog("Death By Captcha password?",default_answer="",hidden=True))),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      ## [[M("GSuite_Financial_Card_Information"),[(eval("""M(("Using Card Ending In {}".format(Get(Shop,shop_abbreviation="%s").GSuite_Financial_Card_Information["Financial_Card_Number"][-4:])),callback=lambda _=None:())if(Get(Shop,shop_abbreviation="%s").GSuite_Financial_Card_Information)else(None)"""%(i.shop_abbreviation,i.shop_abbreviation))),[M("Use Existing"),[eval("""M("%s",callback=lambda _=None:[Update(Get(Shop,shop_abbreviation="%s"),GSuite_Financial_Card_Information=[c for c in oset(listminus(flatten(keymulti(["AliExpress_Financial_Card_Information","GSuite_Financial_Card_Information","Shopify_Financial_Card_Information","Facebook_Financial_Card_Information",], All(Shop)),1),[None])) if c["Financial_Card_Number"][-4:]=="%s"][0]),globals()["ryle"].set_menu()])"""%(a["Financial_Card_Number"][-4:],i.shop_abbreviation,a["Financial_Card_Number"][-4:])) for a in oset(listminus(flatten(keymulti(["AliExpress_Financial_Card_Information","GSuite_Financial_Card_Information","Shopify_Financial_Card_Information","Facebook_Financial_Card_Information",], All(Shop)),1),[None]))]],eval("""M("Add New", callback=lambda _=None:[Update(Get(Shop,shop_abbreviation="%s"),GSuite_Financial_Card_Information = {"Financial_Card_Number": OSA.display_dialog("Financial Card Number?",default_answer="",hidden=True),"Financial_Card_Expiration_Date": OSA.display_dialog("Financial Card Expiration Date [for example: 0125]?",default_answer="",hidden=True),"Financial_Card_CVV": OSA.display_dialog("Financial Card CVV?",default_answer="",hidden=True),"Financial_Card_Billing_First_Name": OSA.display_dialog("Financial Card Billing First Name?",default_answer="").title(),"Financial_Card_Billing_Last_Name": OSA.display_dialog("Financial Card Billing Last Name?",default_answer="").title(),"Financial_Card_Billing_Street_Address": OSA.display_dialog("Financial Card Billing Street Address?",default_answer=""),"Financial_Card_Billing_Street_Address_Line_2": OSA.display_dialog("Financial Card Billing Street Address Line 2 [enter in blank if this does not apply]?",default_answer=""),"Financial_Card_Billing_Country": OSA.display_dialog("Financial Card Billing Country?",default_answer=""),"Financial_Card_Billing_State": OSA.display_dialog("Financial Card Billing State [for example: New York]?",default_answer="").title(),"Financial_Card_Billing_City": OSA.display_dialog("Financial Card Billing City?",default_answer="").title(),"Financial_Card_Billing_ZIP_Code": Integer(OSA.display_dialog("Financial Card Billing ZIP Code?",default_answer="")),}),globals()["ryle"].set_menu()])"""%(i.shop_abbreviation))]]]+\
      ## [[M("Shopify_Financial_Card_Information"),[(eval("""M(("Using Card Ending In {}".format(Get(Shop,shop_abbreviation="%s").Shopify_Financial_Card_Information["Financial_Card_Number"][-4:])),callback=lambda _=None:())if(Get(Shop,shop_abbreviation="%s").Shopify_Financial_Card_Information)else(None)"""%(i.shop_abbreviation,i.shop_abbreviation))),[M("Use Existing"),[eval("""M("%s",callback=lambda _=None:[Update(Get(Shop,shop_abbreviation="%s"),Shopify_Financial_Card_Information=[c for c in oset(listminus(flatten(keymulti(["AliExpress_Financial_Card_Information","GSuite_Financial_Card_Information","Shopify_Financial_Card_Information","Facebook_Financial_Card_Information",], All(Shop)),1),[None])) if c["Financial_Card_Number"][-4:]=="%s"][0]),globals()["ryle"].set_menu()])"""%(a["Financial_Card_Number"][-4:],i.shop_abbreviation,a["Financial_Card_Number"][-4:])) for a in oset(listminus(flatten(keymulti(["AliExpress_Financial_Card_Information","GSuite_Financial_Card_Information","Shopify_Financial_Card_Information","Facebook_Financial_Card_Information",], All(Shop)),1),[None]))]],eval("""M("Add New", callback=lambda _=None:[Update(Get(Shop,shop_abbreviation="%s"),Shopify_Financial_Card_Information = {"Financial_Card_Number": OSA.display_dialog("Financial Card Number?",default_answer="",hidden=True),"Financial_Card_Expiration_Date": OSA.display_dialog("Financial Card Expiration Date [for example: 0125]?",default_answer="",hidden=True),"Financial_Card_CVV": OSA.display_dialog("Financial Card CVV?",default_answer="",hidden=True),"Financial_Card_Billing_First_Name": OSA.display_dialog("Financial Card Billing First Name?",default_answer="").title(),"Financial_Card_Billing_Last_Name": OSA.display_dialog("Financial Card Billing Last Name?",default_answer="").title(),"Financial_Card_Billing_Street_Address": OSA.display_dialog("Financial Card Billing Street Address?",default_answer=""),"Financial_Card_Billing_Street_Address_Line_2": OSA.display_dialog("Financial Card Billing Street Address Line 2 [enter in blank if this does not apply]?",default_answer=""),"Financial_Card_Billing_Country": OSA.display_dialog("Financial Card Billing Country?",default_answer=""),"Financial_Card_Billing_State": OSA.display_dialog("Financial Card Billing State [for example: New York]?",default_answer="").title(),"Financial_Card_Billing_City": OSA.display_dialog("Financial Card Billing City?",default_answer="").title(),"Financial_Card_Billing_ZIP_Code": Integer(OSA.display_dialog("Financial Card Billing ZIP Code?",default_answer="")),}),globals()["ryle"].set_menu()])"""%(i.shop_abbreviation))]]]+\
      ## [[M("Facebook_Financial_Card_Information"),[(eval("""M(("Using Card Ending In {}".format(Get(Shop,shop_abbreviation="%s").Facebook_Financial_Card_Information["Financial_Card_Number"][-4:])),callback=lambda _=None:())if(Get(Shop,shop_abbreviation="%s").Facebook_Financial_Card_Information)else(None)"""%(i.shop_abbreviation,i.shop_abbreviation))),[M("Use Existing"),[eval("""M("%s",callback=lambda _=None:[Update(Get(Shop,shop_abbreviation="%s"),Facebook_Financial_Card_Information=[c for c in oset(listminus(flatten(keymulti(["AliExpress_Financial_Card_Information","GSuite_Financial_Card_Information","Shopify_Financial_Card_Information","Facebook_Financial_Card_Information",], All(Shop)),1),[None])) if c["Financial_Card_Number"][-4:]=="%s"][0]),globals()["ryle"].set_menu()])"""%(a["Financial_Card_Number"][-4:],i.shop_abbreviation,a["Financial_Card_Number"][-4:])) for a in oset(listminus(flatten(keymulti(["AliExpress_Financial_Card_Information","GSuite_Financial_Card_Information","Shopify_Financial_Card_Information","Facebook_Financial_Card_Information",], All(Shop)),1),[None]))]],eval("""M("Add New", callback=lambda _=None:[Update(Get(Shop,shop_abbreviation="%s"),Facebook_Financial_Card_Information = {"Financial_Card_Number": OSA.display_dialog("Financial Card Number?",default_answer="",hidden=True),"Financial_Card_Expiration_Date": OSA.display_dialog("Financial Card Expiration Date [for example: 0125]?",default_answer="",hidden=True),"Financial_Card_CVV": OSA.display_dialog("Financial Card CVV?",default_answer="",hidden=True),"Financial_Card_Billing_First_Name": OSA.display_dialog("Financial Card Billing First Name?",default_answer="").title(),"Financial_Card_Billing_Last_Name": OSA.display_dialog("Financial Card Billing Last Name?",default_answer="").title(),"Financial_Card_Billing_Street_Address": OSA.display_dialog("Financial Card Billing Street Address?",default_answer=""),"Financial_Card_Billing_Street_Address_Line_2": OSA.display_dialog("Financial Card Billing Street Address Line 2 [enter in blank if this does not apply]?",default_answer=""),"Financial_Card_Billing_Country": OSA.display_dialog("Financial Card Billing Country?",default_answer=""),"Financial_Card_Billing_State": OSA.display_dialog("Financial Card Billing State [for example: New York]?",default_answer="").title(),"Financial_Card_Billing_City": OSA.display_dialog("Financial Card Billing City?",default_answer="").title(),"Financial_Card_Billing_ZIP_Code": Integer(OSA.display_dialog("Financial Card Billing ZIP Code?",default_answer="")),}),globals()["ryle"].set_menu()])"""%(i.shop_abbreviation))]]]+\
      ## [[M("AliExpress_Financial_Card_Information"),[(eval("""M(("Using Card Ending In {}".format(Get(Shop,shop_abbreviation="%s").AliExpress_Financial_Card_Information["Financial_Card_Number"][-4:])),callback=lambda _=None:())if(Get(Shop,shop_abbreviation="%s").AliExpress_Financial_Card_Information)else(None)"""%(i.shop_abbreviation,i.shop_abbreviation))),[M("Use Existing"),[eval("""M("%s",callback=lambda _=None:[Update(Get(Shop,shop_abbreviation="%s"),AliExpress_Financial_Card_Information=[c for c in oset(listminus(flatten(keymulti(["AliExpress_Financial_Card_Information","GSuite_Financial_Card_Information","Shopify_Financial_Card_Information","Facebook_Financial_Card_Information",], All(Shop)),1),[None])) if c["Financial_Card_Number"][-4:]=="%s"][0]),globals()["ryle"].set_menu()])"""%(a["Financial_Card_Number"][-4:],i.shop_abbreviation,a["Financial_Card_Number"][-4:])) for a in oset(listminus(flatten(keymulti(["AliExpress_Financial_Card_Information","GSuite_Financial_Card_Information","Shopify_Financial_Card_Information","Facebook_Financial_Card_Information",], All(Shop)),1),[None]))]],eval("""M("Add New", callback=lambda _=None:[Update(Get(Shop,shop_abbreviation="%s"),AliExpress_Financial_Card_Information = {"Financial_Card_Number": OSA.display_dialog("Financial Card Number?",default_answer="",hidden=True),"Financial_Card_Expiration_Date": OSA.display_dialog("Financial Card Expiration Date [for example: 0125]?",default_answer="",hidden=True),"Financial_Card_CVV": OSA.display_dialog("Financial Card CVV?",default_answer="",hidden=True),"Financial_Card_Billing_First_Name": OSA.display_dialog("Financial Card Billing First Name?",default_answer="").title(),"Financial_Card_Billing_Last_Name": OSA.display_dialog("Financial Card Billing Last Name?",default_answer="").title(),"Financial_Card_Billing_Street_Address": OSA.display_dialog("Financial Card Billing Street Address?",default_answer=""),"Financial_Card_Billing_Street_Address_Line_2": OSA.display_dialog("Financial Card Billing Street Address Line 2 [enter in blank if this does not apply]?",default_answer=""),"Financial_Card_Billing_Country": OSA.display_dialog("Financial Card Billing Country?",default_answer=""),"Financial_Card_Billing_State": OSA.display_dialog("Financial Card Billing State [for example: New York]?",default_answer="").title(),"Financial_Card_Billing_City": OSA.display_dialog("Financial Card Billing City?",default_answer="").title(),"Financial_Card_Billing_ZIP_Code": Integer(OSA.display_dialog("Financial Card Billing ZIP Code?",default_answer="")),}),globals()["ryle"].set_menu()])"""%(i.shop_abbreviation))]]]+\
      # eval("""[M("Push Shopify Store Changes", callback=lambda _=None: [firefox65_do('Shop()("%s").Migrate_Shopify_Changes(possible_fields=Shop()("%s").Fields_To_Update,quit=True)'),Update(Shop()("%s"),Fields_To_Change=[])])
      #   ]"""%(i.shop_abbreviation, i.shop_abbreviation, i.shop_abbreviation)) + \
      # eval("""[[M("Run Setup"), M("Run Setup", callback=lambda _=None:[helper(lambda:(Get(Shop,shop_abbreviation="%s").Run_Setup ()) ),Update(Get(Shop,shop_abbreviation="%s"),Fields_To_Update=[]),globals()["ryle"].set_menu()])]]"""%(i.shop_abbreviation,i.shop_abbreviation)) + \
      #eval("""[[M("Delete Shop"), M("Delete Shop", callback=lambda _=None:[([Del(Get(Shop,shop_abbreviation="%s")),globals()["ryle"].set_menu()])if(OSA.display_dialog("Are you sure you want to delete your shop? Please enter in Delete My Shop to delete your shop.",default_answer="")=="Delete My Shop")else()])]]"""%(i.shop_abbreviation)) + \
      eval("""[[M("Active"), [M("Help", callback=lambda _=None:OSA.display_dialog("Is this shop active?",text_prompt=False)), (False)if(Get(Shop, shop_abbreviation="%s").Active==False)else(True), M("Update", callback=lambda _=None:[Update(Get(Shop, shop_abbreviation="%s"),Active=((True)if(OSA.display_dialog("Is this shop active?",text_prompt=False,buttons=["No","Yes"])=="Yes")else(False)),Fields_To_Update=(Get(Shop,shop_abbreviation="%s").Fields_To_Update)+["Active"]),globals()["ryle"].set_menu()]) ]]]"""%(i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation)) + \
      [[M("Price Changes"),eval("""[M("+",callback=lambda _=None:[OSA().display_dialog("Success",text_prompt=0) if tryreturn(lambda:PriceChange.flow(OSA.display_dialog(q='Please enter in either one price change or a list. you can also copy paste from excel.\\nEach line in this dialog should include a price number or range like 0-5 and a colon and then either just a number or an equation with x in it.\\nA range like 0-5 will be 0.01 to 5.00 so 0 will not be included but 5 will be. Anywhere from 0.01 to 5.00 will return a new price that you determine.\\nIf you are copy pasting from Excel, row A should contain the colon (eg: 0-5:) and row B should contain the price or equation (eg: x+5 or 10).\\n\\nThe following are examples:\\n0-5: 10          (between 0.01 and 5, including 5 will return 10.)\\n0-5: (x*2)+5     (multiply it by 2 and then add 5.)\\n0-5: (x+5)*1.5   (add 5 and then multiply it by 1.5)\\n5: x*2           (for 5, multiply it by 2)\\n5: x+2           (add 2 to it)\\n5-15: x+15       (between 5.01 and 15, including 15, add 15)\\n\\n\\nnote: The max price supported is $10000.',default_answer="\\n"*45),shop="%s"))==True else OSA.display_dialog("There was an error. Please try again.",text_prompt=False),self.set_menu()])]"""%(i.shop_abbreviation))  +  eval("""[M("Delete All", callback= lambda _=None: [lmap(Del,Filter(PriceChange,shop="%s")),self.set_menu()])]"""%(i.shop_abbreviation))  +  eval("""[[M("Price Change Rounding"), [M("Help",callback=lambda _=None:OSA.display_dialog("Round the price after changing it? You can round the price up, round the price down, or round the price up if it's over 50 cents and down if it's under 50 cents.",text_prompt=False)),M("Current: %s"),M("Leave Price as is",callback=lambda _=None:[Update(Get(Shop,shop_abbreviation="%s"),Price_Change_Round_Type=None),self.set_menu()]),M("Round Up",callback=lambda _=None:[Update(Get(Shop,shop_abbreviation="%s"),Price_Change_Round_Type="up"),self.set_menu()]),M("Round Down",callback=lambda _=None:[Update(Get(Shop,shop_abbreviation="%s"),Price_Change_Round_Type="down"),self.set_menu()]),M("Round Up if ends with over 0.5",callback=lambda _=None:[Update(Get(Shop,shop_abbreviation="%s"),Price_Change_Round_Type="round"),self.set_menu()])]]]"""%(i.Price_Change_Round_Type,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation,i.shop_abbreviation))  +  eval("""[[M("Price Change Ending Amount"), [M("Help",callback=lambda _=None:OSA.display_dialog("Enter the ending amount. If this is on, it will round the number up and subtract. .99 will make $4.10 $4.99 or $3.98 $3.99 or $4.50 $4.99. An empty field will turn this off. [for example: .99, .95, .90]",text_prompt=False)),M("Change Ending Amount: {}".format("on, %s (click to turn off/adjust)"if(Get(Shop,shop_abbreviation="%s").Price_Change_Ending_Amount!=None)else("off (click to turn on/adjust value)")),callback=lambda _=None:[Update(Get(Shop,shop_abbreviation="%s"),Price_Change_Ending_Amount=[globalise(OSA.display_dialog("Enter the ending amount. If this is on, it will round the number up and subtract. .99 will make $4.10 $4.99 or $3.98 $3.99 or $4.50 $4.99. An empty field will turn this off. [for example: .99, .95, .90]",default_answer=".99"),"price_change_ending_amount"),(None)if(globe("price_change_ending_amount")=="")else(globe("price_change_ending_amount"))][1]),self.set_menu()])]]]"""%(i.Price_Change_Ending_Amount,i.shop_abbreviation,i.shop_abbreviation))  +  eval("""[M("Test A Price",callback = lambda _=None:[OSA.display_dialog("$"+str(CH().price_change(round(float(OSA.display_dialog("Enter a price",default_answer="")),2),"%s")),text_prompt=False)])]"""%(i.shop_abbreviation))  +  eval("""[M("Copy Current Price Change List", callback = lambda _=None: PriceChange().get_current_pricechanges("%s"))]"""%(i.shop_abbreviation))]],

      ]
      
                for i in All(Shop)        ]
  class SalesBar:
    # Basically, it shows the day's sales for all shops, as well and if clicked, shows the adsets.
    def __init__(self):
      import rumps
      from rumps import MenuItem as M
      from rumps import MenuItem
      self.app = rumps.App("🍃",quit_button=Null)
      globals().update(locals())


      self.set_menu()
      #process(  lambda: [time.sleep(6.15), self.set_menu()]  )
      process(lambda: [[time.sleep(60),self.set_menu()] for i in range(WHILE_TRUE)])
      time.sleep(4.5)
      self.app.run()


    def set_menu(self):
      keys = list(self.app.menu.keys())
      redprint(keys)
      for i in keys:
        self.app.menu.pop(i)
      #time.sleep(2)
      keycall("Icon",All(Adset));#@Refresh Icons
      keycall("post_handle",All(Adset))
      self.app.title = "/".join(["%s"%(round(sum(list(map(Float,key("total_price",Filter(Order,created_at__gte=Date()(),shop=i.shop_abbreviation))))),2) ) for i in All(Shop)])
      #@[2018.12.9 4:34 AM]Okay, it seems like if only the source adset shows the duplicates, I need to show all adsets, not only the active ones, so it will be easier to have each instance of the item show a duplicate adset list with metrics; and there will be no overlap of duplicate adset list from any source adset, ie: i have source adset brick, if at any time another adset with this handle and unmatching targeting appears, it will stem from a New source adset, therefore there is no overlap in terms of: filter-getting the adsetinsight by way of: Filter(Adset,source_adset_id=i.adset_id) & then the associated Adsetinsights from those.
      #@[2018.12.9 4:40 AM]This is tested.
      self.app.menu = [MenuItem("/",callback=lambda _=None:[pool(lambda i:July_Adset_Utilities().update_advertisement_all(i.adset_id),Filter(Adset,status="ACTIVE")).result(),self.set_menu()])] + \
                      [setitem(g(),"salesbar_x",self),
                      [
                        [MenuItem(title="%s%s;%s;%s|%s|%s"%("*"if(not i.original_caid and not i.source_adset_id)else "**" if(i.source_adset_id and not i.original_caid) else "",
                          idx+1,1+(-1*(Date()-i.created_time)),
                          round(sum(sud("spend",Filter(Adsetinsight,adset_id=i.adset_id))),2),
                          round(sum(sud("website_purchase_value",Filter(Adsetinsight,adset_id=i.adset_id))),2),
                          round(sum(sud("website_purchase",Filter(Adsetinsight,adset_id=i.adset_id))),2)
                          ),icon="%s"%i.icon), 
                            [
                              [MenuItem("%s;%s|%s|%s"%(sudsort("date",Filter(Adsetinsight,adset_id=i.adset_id),tcer=True)[0].date,
                                                        sudsort("date",Filter(Adsetinsight,adset_id=i.adset_id),tcer=True)[0].spend,
                                                        sudsort("date",Filter(Adsetinsight,adset_id=i.adset_id),tcer=True)[0].website_purchase_value,
                                                        sudsort("date",Filter(Adsetinsight,adset_id=i.adset_id),tcer=True)[0].website_purchase, )), 
                              eval('[MenuItem("+",callback=lambda _=None:[Get(Adset,adset_id=%s).post_duplicate(),g()["salesbar_x"].set_menu()])]'%(i.adset_id),globals())+\
                              [MenuItem("%s|%s|%s|%s|%s"%(b.adset_id,b.date,b.spend,b.website_purchase_value,b.website_purchase)) for a in Filter(Adset,source_adset_id= [i for i in Filter(Adset,handle=i.handle) if (not i.original_caid and not i.source_adset_id)][0].adset_id ) for b in keysort("date",Filter(Adsetinsight,adset_id=a.adset_id),tcer=True)] \
                              if Filter(Adset,source_adset_id=[i for i in Filter(Adset,handle=i.handle) if (not i.original_caid and not i.source_adset_id)][0].adset_id) else \
                              eval('[MenuItem("+",callback=lambda _=None:[Get(Adset,adset_id=%s).post_duplicate(),g()["salesbar_x"].set_menu()])]'%(i.adset_id),globals()) ] if Filter(Adsetinsight,adset_id=i.adset_id)else \
                                      (MenuItem("Waiting For Adsetinsight Data")),

                              [MenuItem(Get(Handle,handle=i.handle).reach),
                                eval('[MenuItem("+",callback=lambda _=None:[Get(Handle,handle="%s").post_lookalike(),g()["salesbar_x"].set_menu()]) if not Get(Handle,handle="%s").has_adset else MenuItem(".")]'%(i.handle,i.handle),globals())+\
                                [MenuItem("%s|%s|%s|%s"%(a,
                                                          sum(sud("spend",Filter(Adsetinsight,adset_id=Get(Adset,original_caid=a).adset_id))),
                                                          sum(sud("website_purchase_value",Filter(Adsetinsight,adset_id=Get(Adset,original_caid=a).adset_id))),
                                                          sum(sud("website_purchase",Filter(Adsetinsight,adset_id=Get(Adset,original_caid=a).adset_id))), )
                                                        ) for a in Get(Handle,handle=i.handle).has_adset if not i.original_caid and \
                                                                                                            # if an adset with custom audience is deleted, then check to include
                                                                                                            a in lmap(int,key("id",flatten(listminus(key("custom_audiences",All(Adset)),None),1)))] ]
                            ]
                        ] \
                        for idx,i in enum(keysort("created_time",Filter(Adset,status="ACTIVE"),tcer=True))
                      ]
                  ][1]
  class SelfHelpTip_Menulet:
    def __init__(self):
      import rumps
      from rumps import MenuItem as M
      from rumps import MenuItem
      self.app = rumps.App("Self Help Tip Menulet", quit_button=Null)
      globals().update(locals())


      self.set_menu()
      time.sleep(7)
      self.app.run()

    def set_menu(self):
      keys = list(self.app.menu.keys())
      redprint(keys)
      self.app.title = All(SelfHelpTip)[0].selfhelptip
      self.app.menu = [
                        eval("""M(Get(SelfHelpTip,id=%s).selfhelptip,callback=lambda _=None:[setattr(self.app,"title",Get(SelfHelpTip,id=%s).selfhelptip)])"""%(i.id,i.id)) for i in All(SelfHelpTip)
                  ]
  class Starralla:
    def __init__(self):
      import rumps
      from rumps import MenuItem as M
      from rumps import MenuItem
      self.app = rumps.App("💫", quit_button=Null)
      globals().update(locals())

      self.set_menu()
      time.sleep(14)
      self.app.run()
    def set_menu(self):
      keycall("refrequenciate",All(LearnWord))
      keys = list(self.app.menu.keys())
      redprint(keys)
      for i in keys:
        self.app.menu.pop(i)
      self.app.menu = [
                        MenuItem("%s: %s"%(i.frequency, i.word.title()),callback=lambda _=None:[[Update(Get(LearnWord,word=i.word),starralla=0),self.set_menu()] if "0"==OSA.display_dialog( (":%s:\n(0/*)\n\n"%(i.word.title()))+("\n\n=============================================\n".join( [(Z+"\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^") if idx!=0 else Z for idx, Z in enum([""]+i.occurations)] ))) else()] ) for i in tcer(keysort("frequency",Filter(LearnWord,starralla=1)) )
                      ]
      """
      LearnWord(date_added=datetime.now(),frequency=1,occurations=["a\na"],starralla=1,word="highfeluctant").save()
      LearnWord(date_added=datetime.now(),frequency=1,occurations=["a\na","b\nb"],starralla=1,word="drastic").save()
      LearnWord(date_added=datetime.now(),frequency=1,occurations=["a\na","b\nb","c\nc"],starralla=1,word="hotbox").save()
      """
  globals().update(locals())
class OSA(object):
  def domain_tests(self):
    OSA("Terminal", ["cmd_n", "delay 2", "nettop", "delay 2", "return"])
    OSA("Google Chrome 70", ["cmd_q"])
    OSA("Google Chrome 70", )
    OSA("Google Chrome 70", ["cmd_l", "delay 2", "cmd_l", "aliexpress.com", "delay 2", "return"])
    redinput("visit 5 items in each category")
    OSA("Google Chrome 70", ["cmd_q"])
    OSA("Google Chrome 70", )
    OSA("Google Chrome 70", ["cmd_q"])
    OSA("Google Chrome 70", )
    OSA("Google Chrome 70", ["cmd_l", "delay 2", "cmd_l", "facebook.com", "delay 2", "return"])
    redinput("scroll down the homepage")
    OSA("Google Chrome 70", ["cmd_q"])
    OSA("Google Chrome 70", )
    OSA("Google Chrome 70", ["cmd_l", "delay 2", "cmd_l", "business.facebook.com", "delay 2", "return"])
    redinput("load the ads manager, the business settings page, the page posts page, and the audience insights page")
    OSA("Google Chrome 70", ["cmd_q"])
    OSA("Google Chrome 70", )
    OSA("Google Chrome 70", ["cmd_l", "delay 2", "cmd_l", "messenger.com", "delay 2", "return"])
    redinput("load messenger.com")
    OSA("Google Chrome 70", ["cmd_l", "delay 2", "cmd_l", "google.com", "delay 2", "return"])
    OSA("Google Chrome 70", ["cmd_l", "delay 2", "cmd_l", "us-proxy.com", "delay 2", "return"])
    OSA("Google Chrome 70", ["cmd_l", "delay 2", "cmd_l", "whensend.com", "delay 2", "return"])
    OSA("Google Chrome 70", ["cmd_q"])
    OSA("Google Chrome 70", )
    OSA("Google Chrome 70", ["cmd_l", "delay 2", "cmd_l", "17track.net", "delay 2", "return"])
    redinput("load the page")
    OSA("Google Chrome 70", ["cmd_q"])
    OSA("Google Chrome 70", )
    OSA("Google Chrome 70", ["cmd_l", "delay 2", "cmd_l", "usps.com", "delay 2", "return"])
    redinput("load the page")
    OSA("Google Chrome 70", ["cmd_q"])
    OSA("Google Chrome 70", )
    OSA("Google Chrome 70", ["cmd_l", "delay 2", "cmd_l", "idcloak.com", "delay 2", "return"])
    redinput("load the page")
    OSA("Google Chrome 70", ["cmd_q"])
    OSA("Google Chrome 70", )
    OSA("Google Chrome 70", ["cmd_l", "delay 2", "cmd_l", "bitly.com", "delay 2", "return"])
    redinput("load the page")
    OSA("Google Chrome 70", ["cmd_l", "delay 2", "https://gmail.com", "delay 2", "return"])
    redinput("log into http://my.jetpack")
  def help(self):
    list(map(redprint, ["arrow","mousepoints","mouserelease","mousesteps_","rightclick_","doubleclick_","click_","brightness","shift_","cmd_","ctrl_","delay","keycode_control","keycode","notify",]))
  def __init__(self, app=None, chain=None):
    from os import system
    self.keycode_map = d = {"esc":"53","f1":"122","f2":"120","f3":"99","f4":"118","f5":"96","f6":"97","f7":"98","f8":"100","f9":"101","f10":"109","f11":"103","f12":"111","~":"50","1":"18","2":"19","3":"20","4":"21","5":"23","6":"22","7":"26","8":"28","9":"25","0":"29","-":"27","=":"24","delete":"51","tab":"48","~":"50","{":"33","}":"30","|":"42",":":"41","\"":"39","_":"27","+":"24","<":"43",">":"47","?":"44","N":"45","M":"46","Q":"12","W":"13","E":"14","R":"15","T":"17","Y":"16","U":"32","I":"34","O":"31","P":"35","A":"0","S":"1","D":"2","F":"3","G":"5","H":"4","J":"38","K":"40","L":"37","Z":"6","X":"7","C":"8","V":"9","B":"11",}
    system("""osascript -e 'tell application "System Events" to activate application "%s"'"""%app) if app != None else None
    if chain is not None:
      for c in chain:
        if 'arrow_' in c:
          self.arrow(c.split('_')[-1], cmd=True) if "cmd" in c else self.arrow(c.split('_')[-1], ctrl=True) if "ctrl" in c else self.arrow(c.split('_')[-1],)
        elif 'mousepoints' == c:
          self.mousepoints()
        elif 'mouserelease' == c:
          self.mouserelease()
        elif 'mousesteps_' in c:
          self.mousesteps(c.split('_')[1], c.split('_')[2], c.split('_')[3])
        elif 'rightclick_' in c:
          self.rightclick(c.split('_')[1], c.split('_')[2])
        elif 'doubleclick_' in c:
          self.doubleclick(c.split('_')[1], c.split('_')[2])
        elif 'click_' in c:
          self.click(c.split('_')[1], c.split('_')[2])
        elif 'activeclick_' in c:
          self.activeclick(c.split('_')[1], c.split('_')[2])
        elif 'brightness' in c:
          self.brightness(c.split(' ')[-1])
        elif 'shift_' in c:
          self.shift_key(c.split('_')[1])
        elif 'cmd_' in c:
          self.cmd_key(c.split('_')[-1])
        elif 'ctrl_' in c:
          self.ctrl_key(c.split('_')[-1])
        elif 'delay' in c:
          self.delay(c.split(' ')[-1])
        elif 'keycode_control_option' in c:
          self.keycode_control_option(c.split('_')[-1])
        elif 'keycode_control' in c:
          self.keycode_control(c.split('_')[-1])
        elif 'keycode_command' in c:
          self.keycode_command(c.split('_')[-1])
        elif 'keycode' in c:
          self.keycode(c.split('_')[-1])
        elif 'notify' in c:
          self.notify(" ".join(c.split(" ")[1:]))
        elif 'systemcommand' in c:
          self.systemcommand("_".join(c.split("_")[1:]))
        elif 'tab' == c:
          self.keystroke_key('tab')
        elif 'return' == c:
          self.keystroke_key('return')
        else:
          pyperclip.copy(c); time.sleep(0.3); self.cmd_key("v"); time.sleep(0.2); strand(lambda: [time.sleep(2), pyperclip.copy("\n")])
          #pyperclip.copy("\n")
          #self.key(c)
  def keycode_control_option(self, x):
    system("""osascript -e 'tell application "System Events" to key code %s using {control down, option down}'""" % self.keycode_map.get(x) )
  def keycode_control(self, x):
    system("""osascript -e 'tell application "System Events" to key code %s using control down'""" % self.keycode_map.get(x) )
  def keycode_command(self, x):
    system("""osascript -e 'tell application "System Events" to key code %s using command down'""" % self.keycode_map.get(x) )
  def keycode(self, x):
    system("""osascript -e 'tell application "System Events" to key code %s'""" % self.keycode_map.get(x) ) # system("""osascript -e 'tell application "System Events" \n key code %s \n end tell'""" % x)
  def arrow(self, direction, cmd=False, ctrl = False):
    if direction == 'left':
      system("""osascript -e 'tell application "System Events" to key code 123%s'"""%(" using command down" if cmd == True else " using control down" if ctrl == True else ""  ))
    if direction == 'right':
      system("""osascript -e 'tell application "System Events" to key code 124%s'"""%(" using command down" if cmd == True else " using control down" if ctrl == True else ""  ))
    if direction == 'up':
      system("""osascript -e 'tell application "System Events" to key code 126%s'"""%(" using command down" if cmd == True else " using control down" if ctrl == True else ""  ))
    if direction == 'down':
      system("""osascript -e 'tell application "System Events" to key code 125%s'"""%(" using command down" if cmd == True else " using control down" if ctrl == True else ""  ))
  def brightness(self, lvl):
    lvl = int(lvl)
    upbrightness = """osascript -e 'tell application "System Events" to key code 144'"""
    downbrightness = """osascript -e 'tell application "System Events" to key code 145'"""
    for i in range(32):
      system(upbrightness)
      time.sleep(0.02)
    time.sleep(1)
    for i in range(32-lvl*2):
      system(downbrightness)
      time.sleep(0.02)
  def delay(self, t):
    system("""osascript -e 'tell application "System Events" to delay %s'"""%t)
  def cmd_key(self, y):
    system("""osascript -e 'tell application "System Events" to keystroke "%s" using {command down}'"""%y)
  def ctrl_key(self, y):
    system("""osascript -e 'tell application "System Events" to keystroke "%s" using {control down}'"""%y)
  def shift_key(self, y):
    system("""osascript -e 'tell application "System Events" to keystroke %s using {shift down}'"""%y)
  def keystroke_key(self, y):
    system("""osascript -e 'tell application "System Events" to keystroke %s'"""%y)
  def key(self, y):
    if y in ['tab', 'return']:
      system("""osascript -e 'tell application "System Events" to keystroke %s'"""%y)
    else:
      system("""osascript -e 'tell application "System Events" to keystroke "%s"'"""%y)
  def mousepoints(self):
    return list(map(int,subprocess.getoutput('~/tavern/tavern/.MouseTools -location').split("\n")))
  def mouserelease(self):
    system('~/tavern/tavern/.MouseTools -releaseMouse')
  def mousesteps(self, steps, x, y):
    system('~/tavern/tavern/.MouseTools -mouseSteps %s -x %s -y %s'%(steps,x,y))
  def rightclick(self, x, y):
    system('~/tavern/tavern/.MouseTools -x %s -y %s -leftClick -controlKey'%(x,y))
  def doubleclick(self, x, y):
    system('~/tavern/tavern/.MouseTools -x %s -y %s -doubleLeftClick'%(x, y))
  def click(self, x, y):
    system('~/tavern/tavern/.MouseTools -x %s -y %s -leftClick'%(x, y))
  def activeclick(self, x, y):
    system('~/tavern/tavern/.MouseTools -x %s -y %s -leftClick'%(x, y))
    system('~/tavern/tavern/.MouseTools -x %s -y %s -leftClick'%(x+1, y))
    system('~/tavern/tavern/.MouseTools -x %s -y %s -leftClick'%(x, y))
  def mousemove(self, x, y):
    a = subprocess.getoutput('~/tavern/tavern/.MouseTools -x %s -y %s'%(x, y))
    if "Error" in a:
      magentaprint(x,y)
  @staticmethod
  def notify(a, b=" ",sound=None, x=True):
    process(lambda: print("OSA() notification: %s"%a))
    a = a.replace("'","’").replace('"',"“")
    b = b.replace("'","’").replace('"',"“")
    if sound == None: process(lambda: system('''osascript -e 'display notification "{}" with title "{}"' '''.format(b,a.replace("'", ""))))
    else: process(lambda: system('''osascript -e 'display notification "{}" with title "{}" sound name "default"' '''.format(b,a.replace("'", ""))))
    process(lambda:[time.sleep(2.5),OSA().clear_all_notifications()])if(x)else()
  @staticmethod
  def display_dialog(q="default dialog prompt", buttons=[ "OK"], text_prompt=True, default_answer="\n\n\n\n\n\n\n\n\n\n\n\n\n", dropdown_options=None, hidden=False, many_options=False):
    # OSA("Finder")


    """ ::: Normally OSAX commands never times out but since you have targeted display dialog to another application OSAX command do timeout. By default when you send an event to another application your script waits for an reply. When there is no reply from the other application within two minutes an timeout error will be returned. However there are events that can take longer than two minutes, so you can lengthen or shorten the wait time of your script before it returns an error. - From Stackoverflow ::: """
    default_answer = default_answer.replace("'","’").replace('"',"“")
    q = q.replace("'","’").replace('"',"“")

    is_dropdown = True if dropdown_options != None else False
    if is_dropdown==True:
      """ ::: HAD TO SLIP THIS IN | ::: """
      option_list = ",".join([ ('"%s"'%i.replace("'","’").replace('"',"“").replace(",","，"))          for i in dropdown_options])
      # `giving up after 200000` failed... syntactically unable tto sure where to upload it.
      #xom = """ osascript -e 'choose from list {%s} with prompt "%s" with multiple selections allowed' """ %  ( option_list , q  ,     ) 
      #xom = 'tell application (path to frontmost application as text)\n    with timeout of 30000 seconds -- wait 500 minutes\n        choose from list {%s} with prompt "%s" with multiple selections allowed\n    end timeout\nend tell'%(option_list,q)
      # process(lambda: [sp(0.00), OSA("Finder"), sp(0.1), OSA("Finder"), sp(0.1), OSA("Finder"), sp(0.1), OSA("Finder"), sp(0.1), OSA("Finder"), sp(0.1), OSA("Finder")])
      
      # process(lambda: [sp(0.00), OSA("Finder")if(OSA().getforemostwindowapp()!="Finder")else(), sp(0.1),  OSA("Finder")if(OSA().getforemostwindowapp()!="Finder")else(), sp(0.1)])
      # OSA("Finder") # permission issues with #
      
      #dropdown_option = subprocess.getoutput("""osascript -e 'tell application (path to frontmost application as text)' -e 'with timeout of 30000 seconds -- wait 500 minutes' -e 'choose from list {%s} with prompt "%s" with multiple selections allowed' -e 'end timeout' -e 'end tell'"""%(option_list,q))
      x = subprocess.check_output("""osascript -e 'tell application (path to frontmost application as text)' -e 'with timeout of 30000 seconds -- wait 500 minutes' -e 'choose from list {%s} with prompt "%s\n\n(Note that for display purposes, any commas in your dropdown options have been replaced with fullwidth commas)" %s' -e 'end timeout' -e 'end tell'"""%(option_list,q,"with multiple selections allowed"if(many_options==True)else("")),shell=True).decode()[:-1]
      ()if(x!="false")else((0/0))
      return lmap(lambda i:i.replace("，",","),x.replace("’","'").replace("“",'"').split(", ")) if many_options==True else x.replace("’","'").replace("“",'"').split("，")[0]
    if text_prompt == False: # BUTTON PROMPT (which may as well be dropdown list prompt)
      # Terminal requires you to focus on the 
      #x = subprocess.getoutput("""osascript -e 'tell application (path to frontmost application as text) to display dialog "%s" default answer "%s" buttons {%s}  giving up after 99969'  """ % (q, default_answer, ",".join(['"%s"'%i for i in buttons])))
      #x = subprocess.getoutput("""osascript -e 'tell application (path to frontmost application as text) to display dialog "%s" default answer "%s" buttons {%s}  giving up after 99969'  """ % (q, default_answer, ",".join(['"%s"'%i for i in buttons])))
      # process(lambda: [sp(0.00), OSA("Finder"), sp(0.1), OSA("Finder"), sp(0.1), OSA("Finder"), sp(0.1), OSA("Finder"), sp(0.1), OSA("Finder"), sp(0.1), OSA("Finder")])
      
      # process(lambda: [sp(0.00), OSA("Finder")if(OSA().getforemostwindowapp()!="Finder")else(), sp(0.1),  OSA("Finder")if(OSA().getforemostwindowapp()!="Finder")else(), sp(0.1)])
      # OSA("Finder")
      
      x=subprocess.check_output("""osascript -e 'tell application (path to frontmost application as text)' -e 'with timeout of 30000 seconds -- wait 500 minutes' -e 'display dialog "%s" buttons {%s}' -e 'end timeout' -e 'end tell'""" % ( q,",".join(['"%s"'%i for i in buttons]) ),shell=True).decode()[:-1]
      x = x.split("button returned:")[1]
      return x        
    else:
      #@find the error
      #try:
      #x = subprocess.getoutput("""osascript -e 'tell application (path to frontmost application as text) to display dialog "%s" default answer "%s" with icon stop buttons {%s} default button "%s" giving up after 99969' """ %(q, default_answer, ",".join(['"%s"'%i for i in buttons]), buttons[-1]))
      #except Exception as e:
      #  OSA.notify(str(e))
      #    f.write(str(e))

      #x = subprocess.getoutput("""osascript -e 'tell application (path to frontmost application as text) to display dialog "%s" default answer "%s" with icon stop buttons {%s} default button "%s" giving up after 99969' """ %(q, default_answer, ",".join(['"%s"'%i for i in buttons]), buttons[-1]))
      #button_returned = x.replace(", gave up:false","").replace(", gave up:true","").split(", text returned:",1)[0].split("button returned:",1)[0]
      #text_returned = x.replace(", gave up:false","").replace(", gave up:true","").split("text returned:",1)[1]
      #OSA().notify(text_returned)
      # process(lambda: [sp(0.00), OSA("Finder"), sp(0.1), OSA("Finder"), sp(0.1), OSA("Finder"), sp(0.1), OSA("Finder"), sp(0.1), OSA("Finder"), sp(0.1), OSA("Finder")])
      
      # process(lambda: [sp(0.00), OSA("Finder")if(OSA().getforemostwindowapp()!="Finder")else(), sp(0.1),  OSA("Finder")if(OSA().getforemostwindowapp()!="Finder")else(), sp(0.1)])
      # OSA("Finder")
      
      x=subprocess.check_output("""osascript -e 'tell application (path to frontmost application as text)' -e 'with timeout of 30000 seconds -- wait 500 minutes' -e 'display dialog "%s" default answer "%s" buttons {%s} %s' -e 'end timeout' -e 'end tell'""" % ( q,default_answer,",".join(['"%s"'%i for i in buttons]), "with hidden answer" if hidden==True else ""),shell=True).decode()[:-1]

      #xom='tell application (path to frontmost application as text)\n    with timeout of 30000 seconds -- wait 500 minutes\n        display dialog "%s" default answer "%s" buttons {%s}\n    end timeout\nend tell'%(q,default_answer,",".join(['"%s"'%i for i in buttons]))
      #open(address,"w").write(xom)
      #os.system("ls {}".format(address))
      #a = subprocess.getoutput("/usr/bin/osascript {}".format(address))
      text_return = x.replace("’","'").replace("“",'"')
      try:
        text_return = text_return.split("text returned:")[1]
      except Exception as e:
        OSA.notify("DisplayDialog Error")
        OSA.notify(text_return)
        pyperclip.copy(text_return)
        0/0
      return text_return
  @staticmethod
  def log(q="default dialog prompt", buttons=[ "OK"], tp=True, df="", do=None, hidden=False, mo=False):
    return OSA().display_dialog(q=q,buttons=buttons,text_prompt=tp,default_answer=df,dropdown_options=do,hidden=hidden,many_options=mo)
  def systemcommand(self, x):
    system(x)
  def exit_preview_windows(self):
    os.system("""osascript -e 'tell application "Preview"' -e 'set mainID to id of front window' -e 'close (every window)' -e 'end tell'""")
  def getforemostwindowtitle(self):
    window_title = subprocess.getoutput('osascript -e \'global frontApp, frontAppName, windowTitle\n\nset windowTitle to ""\ntell application "System Events"\n    set frontApp to first application process whose frontmost is true\n    set frontAppName to name of frontApp\n    tell process frontAppName\n        tell (1st window whose value of attribute "AXMain" is true)\n            set windowTitle to value of attribute "AXTitle"\n        end tell\n    end tell\nend tell\'')
    #print(window_title)
    return window_title
  def getforemostwindowapp(self):
    app_title = subprocess.getoutput("""osascript -e 'tell application "System Events" to set frontApp to name of first application process whose frontmost is true'""")
    #print(app_title)
    return app_title
  def getwindowarrangement(self, app):
    window_position = subprocess.getoutput("""osascript -e 'tell application "System Events" to tell application process "%s" to get position of window 1'""" % app).split(", ")
    window_size = subprocess.getoutput("""osascript -e 'tell application "System Events" to tell application process "%s" to get size of window 1'""" % app).split(", ")
    window_position = list(map(int, window_position))
    window_size = list(map(int, window_size))
    window_size[0] = window_size[0] + window_position[0]
    window_size[1] = window_size[1] + window_position[1]
    window_arrangement = window_position + window_size
    #print(window_arrangement)
    return window_arrangement
  def getwindowsize(self, app):
    x = subprocess.getoutput("""osascript -e 'tell application "System Events" to tell application process "%s" to get size of window 1'""" % app).split(", ")
    if "Can’t get application process %s"%(app) in x:
      return self.getwindowsize(app)
    return x
  def getwindowarrangements(self):
    window_arrangements = []
    redprint("||  Return on foremost window app 'Finder'")
    while True:
      foremostwindowtitle = self.getforemostwindowtitle()
      window_arrangement = self.getwindowarrangement(self.getforemostwindowapp())
      info = [foremostwindowtitle] + window_arrangement
      if info not in window_arrangements:
        window_arrangements .  append( info)
        print(window_arrangements)
      if self.getforemostwindowapp() == "Finder":
        return window_arrangements
  def setforemostwindowarrangement(self, app, x, y, w, h):
    system("""osascript -e 'tell application "%s" to set bounds of front window to {%s, %s, %s, %s}'""" % (app, x, y, w, h))
  def setwindowdesktop(self, app, desktop):
    pass
  def clear_all_notifications(self):
    os.system("""osascript -e 'tell application "System Events"' -e 'tell process "NotificationCenter"' -e 'set numwins to (count windows)' -e 'repeat with i from numwins to 1 by -1' -e 'try' -e 'click button "Close" of window i' -e 'end try' -e 'end repeat' -e 'end tell' -e 'end tell' &> /dev/null &""")
  def new_terminal(self):
    #x = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n<dict>\n\t<key>ANSIBrightRedColor</key>\n\t<data>\n\tYnBsaXN0MDDUAQIDBAUGKyxYJHZlcnNpb25YJG9iamVjdHNZJGFyY2hpdmVyVCR0b3AS\n\tAAGGoKcHCBMZHSQoVSRudWxs1QkKCwwNDg8QERJcTlNDb21wb25lbnRzVU5TUkdCXE5T\n\tQ29sb3JTcGFjZV8QEk5TQ3VzdG9tQ29sb3JTcGFjZVYkY2xhc3NPEB0wLjg4NzY3MjE2\n\tNDggMC45NjI3ODAyMzA0IDEgMU8QHDAuODQxNTU1MjM3OCAwLjk1NzU3MTU2NjEgMQAQ\n\tAYACgAbTFA0VFhcYVU5TSUNDWU5TU3BhY2VJRIADgAUQDNIaDRscV05TLmRhdGFPEQIk\n\tAAACJGFwcGwEAAAAbW50clJHQiBYWVogB98ACgAOAA0ACAA5YWNzcEFQUEwAAAAAQVBQ\n\tTAAAAAAAAAAAAAAAAAAAAAAAAPbWAAEAAAAA0y1hcHBs5bsOmGe9Rs1LvkRuvRt1mAAA\n\tAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKZGVzYwAAAPwAAABlY3BydAAAAWQA\n\tAAAjd3RwdAAAAYgAAAAUclhZWgAAAZwAAAAUZ1hZWgAAAbAAAAAUYlhZWgAAAcQAAAAU\n\tclRSQwAAAdgAAAAgY2hhZAAAAfgAAAAsYlRSQwAAAdgAAAAgZ1RSQwAAAdgAAAAgZGVz\n\tYwAAAAAAAAALRGlzcGxheSBQMwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\tAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB0\n\tZXh0AAAAAENvcHlyaWdodCBBcHBsZSBJbmMuLCAyMDE1AABYWVogAAAAAAAA81EAAQAA\n\tAAEWzFhZWiAAAAAAAACD3wAAPb////+7WFlaIAAAAAAAAEq/AACxNwAACrlYWVogAAAA\n\tAAAAKDgAABELAADIuXBhcmEAAAAAAAMAAAACZmYAAPKwAAANUAAAE7YAAAn8c2YzMgAA\n\tAAAAAQxCAAAF3v//8yYAAAeTAAD9kP//+6L///2jAAAD3AAAwG6ABNIeHyAhWiRjbGFz\n\tc25hbWVYJGNsYXNzZXNdTlNNdXRhYmxlRGF0YaMgIiNWTlNEYXRhWE5TT2JqZWN00h4f\n\tJSZcTlNDb2xvclNwYWNloicjXE5TQ29sb3JTcGFjZdIeHykqV05TQ29sb3KiKSNfEA9O\n\tU0tleWVkQXJjaGl2ZXLRLS5Ucm9vdIABAAgAEQAaACMALQAyADcAPwBFAFAAXQBjAHAA\n\thQCMAKwAywDNAM8A0QDYAN4A6ADqAOwA7gDzAPsDIwMlAyoDNQM+A0wDUANXA2ADZQNy\n\tA3UDggOHA48DkgOkA6cDrAAAAAAAAAIBAAAAAAAAAC8AAAAAAAAAAAAAAAAAAAOu\n\t</data>\n\t<key>BackgroundBlur</key>\n\t<real>0.0</real>\n\t<key>BackgroundColor</key>\n\t<data>\n\tYnBsaXN0MDDUAQIDBAUGKSpYJHZlcnNpb25YJG9iamVjdHNZJGFyY2hpdmVyVCR0b3AS\n\tAAGGoKcHCBMXGyImVSRudWxs1QkKCwwNDg8QERJcTlNDb21wb25lbnRzVU5TUkdCXE5T\n\tQ29sb3JTcGFjZV8QEk5TQ3VzdG9tQ29sb3JTcGFjZVYkY2xhc3NPECgwLjk4NDMxMzcy\n\tNjQgMC45Njg2Mjc0NTI5IDAuOTY0NzA1ODg0NSAxTxAnMC45ODM4MDA3Njg5IDAuOTU5\n\tNTM2MTk0OCAwLjk1NDY3MTIwNDEAEAGAAoAG0hQNFRZVTlNJQ0OAA4AF0hgNGRpXTlMu\n\tZGF0YU8RDzAAAA8wYXBwbAIQAABtbnRyUkdCIFhZWiAH4gAGABYACwAFAB5hY3NwQVBQ\n\tTAAAAABBUFBMAAAAAAAAAAAAAAAAAAAAAAAA9tYAAQAAAADTLWFwcGwAAAAAAAAAAAAA\n\tAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABFkZXNjAAABUAAAAGJk\n\tc2NtAAABtAAABBhjcHJ0AAAFzAAAACN3dHB0AAAF8AAAABRyWFlaAAAGBAAAABRnWFla\n\tAAAGGAAAABRiWFlaAAAGLAAAABRyVFJDAAAGQAAACAxhYXJnAAAOTAAAACB2Y2d0AAAO\n\tbAAAADBuZGluAAAOnAAAAD5jaGFkAAAO3AAAACxtbW9kAAAPCAAAAChiVFJDAAAGQAAA\n\tCAxnVFJDAAAGQAAACAxhYWJnAAAOTAAAACBhYWdnAAAOTAAAACBkZXNjAAAAAAAAAAhE\n\taXNwbGF5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\tAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAbWx1YwAAAAAAAAAiAAAA\n\tDGhySFIAAAAUAAABqGtvS1IAAAAMAAABvG5iTk8AAAASAAAByGlkAAAAAAASAAAB2mh1\n\tSFUAAAAUAAAB7GNzQ1oAAAAWAAACAGRhREsAAAAcAAACFnVrVUEAAAAcAAACMmFyAAAA\n\tAAAUAAACTml0SVQAAAAUAAACYnJvUk8AAAASAAACdm5sTkwAAAAWAAACiGhlSUwAAAAW\n\tAAACnmVzRVMAAAASAAACdmZpRkkAAAAQAAACtHpoVFcAAAAMAAACxHZpVk4AAAAOAAAC\n\t0HNrU0sAAAAWAAAC3npoQ04AAAAMAAACxHJ1UlUAAAAkAAAC9GZyRlIAAAAWAAADGG1z\n\tAAAAAAASAAADLmNhRVMAAAAYAAADQHRoVEgAAAAMAAADWGVzWEwAAAASAAACdmRlREUA\n\tAAAQAAADZGVuVVMAAAASAAADdHB0QlIAAAAYAAADhnBsUEwAAAASAAADnmVsR1IAAAAi\n\tAAADsHN2U0UAAAAQAAAD0nRyVFIAAAAUAAAD4mphSlAAAAAMAAAD9nB0UFQAAAAWAAAE\n\tAgBMAEMARAAgAHUAIABiAG8AagBpzuy37AAgAEwAQwBEAEYAYQByAGcAZQAtAEwAQwBE\n\tAEwAQwBEACAAVwBhAHIAbgBhAFMAegDtAG4AZQBzACAATABDAEQAQgBhAHIAZQB2AG4A\n\t/QAgAEwAQwBEAEwAQwBEAC0AZgBhAHIAdgBlAHMAawDmAHIAbQQaBD4EOwRMBD4EQAQ+\n\tBDIEOAQ5ACAATABDAEQgDwBMAEMARAAgBkUGRAZIBkYGKQBMAEMARAAgAGMAbwBsAG8A\n\tcgBpAEwAQwBEACAAYwBvAGwAbwByAEsAbABlAHUAcgBlAG4ALQBMAEMARCAPAEwAQwBE\n\tACAF5gXRBeIF1QXgBdkAVgDkAHIAaQAtAEwAQwBEX2mCcgAgAEwAQwBEAEwAQwBEACAA\n\tTQDgAHUARgBhAHIAZQBiAG4A/QAgAEwAQwBEBCYEMgQ1BEIEPQQ+BDkAIAQWBBoALQQ0\n\tBDgEQQQ/BDsENQQ5AEwAQwBEACAAYwBvAHUAbABlAHUAcgBXAGEAcgBuAGEAIABMAEMA\n\tRABMAEMARAAgAGUAbgAgAGMAbwBsAG8AcgBMAEMARAAgDioONQBGAGEAcgBiAC0ATABD\n\tAEQAQwBvAGwAbwByACAATABDAEQATABDAEQAIABDAG8AbABvAHIAaQBkAG8ASwBvAGwA\n\tbwByACAATABDAEQDiAOzA8cDwQPJA7wDtwAgA78DuAPMA70DtwAgAEwAQwBEAEYA5ABy\n\tAGcALQBMAEMARABSAGUAbgBrAGwAaQAgAEwAQwBEMKsw6TD8AEwAQwBEAEwAQwBEACAA\n\tYQAgAEMAbwByAGUAc3RleHQAAAAAQ29weXJpZ2h0IEFwcGxlIEluYy4sIDIwMTgAAFhZ\n\tWiAAAAAAAADzFgABAAAAARbKWFlaIAAAAAAAAIOHAAA9qf///7tYWVogAAAAAAAAS+UA\n\tALPvAAAK3VhZWiAAAAAAAAAnagAADmgAAMiVY3VydgAAAAAAAAQAAAAABQAKAA8AFAAZ\n\tAB4AIwAoAC0AMgA2ADsAQABFAEoATwBUAFkAXgBjAGgAbQByAHcAfACBAIYAiwCQAJUA\n\tmgCfAKMAqACtALIAtwC8AMEAxgDLANAA1QDbAOAA5QDrAPAA9gD7AQEBBwENARMBGQEf\n\tASUBKwEyATgBPgFFAUwBUgFZAWABZwFuAXUBfAGDAYsBkgGaAaEBqQGxAbkBwQHJAdEB\n\t2QHhAekB8gH6AgMCDAIUAh0CJgIvAjgCQQJLAlQCXQJnAnECegKEAo4CmAKiAqwCtgLB\n\tAssC1QLgAusC9QMAAwsDFgMhAy0DOANDA08DWgNmA3IDfgOKA5YDogOuA7oDxwPTA+AD\n\t7AP5BAYEEwQgBC0EOwRIBFUEYwRxBH4EjASaBKgEtgTEBNME4QTwBP4FDQUcBSsFOgVJ\n\tBVgFZwV3BYYFlgWmBbUFxQXVBeUF9gYGBhYGJwY3BkgGWQZqBnsGjAadBq8GwAbRBuMG\n\t9QcHBxkHKwc9B08HYQd0B4YHmQesB78H0gflB/gICwgfCDIIRghaCG4IggiWCKoIvgjS\n\tCOcI+wkQCSUJOglPCWQJeQmPCaQJugnPCeUJ+woRCicKPQpUCmoKgQqYCq4KxQrcCvML\n\tCwsiCzkLUQtpC4ALmAuwC8gL4Qv5DBIMKgxDDFwMdQyODKcMwAzZDPMNDQ0mDUANWg10\n\tDY4NqQ3DDd4N+A4TDi4OSQ5kDn8Omw62DtIO7g8JDyUPQQ9eD3oPlg+zD88P7BAJECYQ\n\tQxBhEH4QmxC5ENcQ9RETETERTxFtEYwRqhHJEegSBxImEkUSZBKEEqMSwxLjEwMTIxND\n\tE2MTgxOkE8UT5RQGFCcUSRRqFIsUrRTOFPAVEhU0FVYVeBWbFb0V4BYDFiYWSRZsFo8W\n\tshbWFvoXHRdBF2UXiReuF9IX9xgbGEAYZRiKGK8Y1Rj6GSAZRRlrGZEZtxndGgQaKhpR\n\tGncanhrFGuwbFBs7G2MbihuyG9ocAhwqHFIcexyjHMwc9R0eHUcdcB2ZHcMd7B4WHkAe\n\tah6UHr4e6R8THz4faR+UH78f6iAVIEEgbCCYIMQg8CEcIUghdSGhIc4h+yInIlUigiKv\n\tIt0jCiM4I2YjlCPCI/AkHyRNJHwkqyTaJQklOCVoJZclxyX3JicmVyaHJrcm6CcYJ0kn\n\teierJ9woDSg/KHEooijUKQYpOClrKZ0p0CoCKjUqaCqbKs8rAis2K2krnSvRLAUsOSxu\n\tLKIs1y0MLUEtdi2rLeEuFi5MLoIuty7uLyQvWi+RL8cv/jA1MGwwpDDbMRIxSjGCMbox\n\t8jIqMmMymzLUMw0zRjN/M7gz8TQrNGU0njTYNRM1TTWHNcI1/TY3NnI2rjbpNyQ3YDec\n\tN9c4FDhQOIw4yDkFOUI5fzm8Ofk6Njp0OrI67zstO2s7qjvoPCc8ZTykPOM9Ij1hPaE9\n\t4D4gPmA+oD7gPyE/YT+iP+JAI0BkQKZA50EpQWpBrEHuQjBCckK1QvdDOkN9Q8BEA0RH\n\tRIpEzkUSRVVFmkXeRiJGZ0arRvBHNUd7R8BIBUhLSJFI10kdSWNJqUnwSjdKfUrESwxL\n\tU0uaS+JMKkxyTLpNAk1KTZNN3E4lTm5Ot08AT0lPk0/dUCdQcVC7UQZRUFGbUeZSMVJ8\n\tUsdTE1NfU6pT9lRCVI9U21UoVXVVwlYPVlxWqVb3V0RXklfgWC9YfVjLWRpZaVm4Wgda\n\tVlqmWvVbRVuVW+VcNVyGXNZdJ114XcleGl5sXr1fD19hX7NgBWBXYKpg/GFPYaJh9WJJ\n\tYpxi8GNDY5dj62RAZJRk6WU9ZZJl52Y9ZpJm6Gc9Z5Nn6Wg/aJZo7GlDaZpp8WpIap9q\n\t92tPa6dr/2xXbK9tCG1gbbluEm5rbsRvHm94b9FwK3CGcOBxOnGVcfByS3KmcwFzXXO4\n\tdBR0cHTMdSh1hXXhdj52m3b4d1Z3s3gReG54zHkqeYl553pGeqV7BHtje8J8IXyBfOF9\n\tQX2hfgF+Yn7CfyN/hH/lgEeAqIEKgWuBzYIwgpKC9INXg7qEHYSAhOOFR4Wrhg6GcobX\n\thzuHn4gEiGmIzokziZmJ/opkisqLMIuWi/yMY4zKjTGNmI3/jmaOzo82j56QBpBukNaR\n\tP5GokhGSepLjk02TtpQglIqU9JVflcmWNJaflwqXdZfgmEyYuJkkmZCZ/JpomtWbQpuv\n\tnByciZz3nWSd0p5Anq6fHZ+Ln/qgaaDYoUehtqImopajBqN2o+akVqTHpTilqaYapoum\n\t/adup+CoUqjEqTepqaocqo+rAqt1q+msXKzQrUStuK4trqGvFq+LsACwdbDqsWCx1rJL\n\tssKzOLOutCW0nLUTtYq2AbZ5tvC3aLfguFm40blKucK6O7q1uy67p7whvJu9Fb2Pvgq+\n\thL7/v3q/9cBwwOzBZ8Hjwl/C28NYw9TEUcTOxUvFyMZGxsPHQce/yD3IvMk6ybnKOMq3\n\tyzbLtsw1zLXNNc21zjbOts83z7jQOdC60TzRvtI/0sHTRNPG1EnUy9VO1dHWVdbY11zX\n\t4Nhk2OjZbNnx2nba+9uA3AXcit0Q3ZbeHN6i3ynfr+A24L3hROHM4lPi2+Nj4+vkc+T8\n\t5YTmDeaW5x/nqegy6LzpRunQ6lvq5etw6/vshu0R7ZzuKO6070DvzPBY8OXxcvH/8ozz\n\tGfOn9DT0wvVQ9d72bfb794r4Gfio+Tj5x/pX+uf7d/wH/Jj9Kf26/kv+3P9t//9wYXJh\n\tAAAAAAADAAAAAmZmAADypwAADVkAABPQAAAKDnZjZ3QAAAAAAAAAAQABAAAAAAAAAAEA\n\tAAABAAAAAAAAAAEAAAABAAAAAAAAAAEAAG5kaW4AAAAAAAAANgAArgAAAFIAAABDwAAA\n\tsMAAACZAAAANgAAAUAAAAFRAAAIzMwACMzMAAjMzAAAAAAAAAABzZjMyAAAAAAABDHIA\n\tAAX4///zHQAAB7oAAP1y///7nf///aQAAAPZAADAcW1tb2QAAAAAAAAGEAAAoDAAAAAA\n\t0h+zAAAAAAAAAAAAAAAAAAAAAACABNIcHR4fWiRjbGFzc25hbWVYJGNsYXNzZXNdTlNN\n\tdXRhYmxlRGF0YaMeICFWTlNEYXRhWE5TT2JqZWN00hwdIyRcTlNDb2xvclNwYWNloiUh\n\tXE5TQ29sb3JTcGFjZdIcHScoV05TQ29sb3KiJyFfEA9OU0tleWVkQXJjaGl2ZXLRKyxU\n\tcm9vdIABAAgAEQAaACMALQAyADcAPwBFAFAAXQBjAHAAhQCMALcA4QDjAOUA5wDsAPIA\n\t9AD2APsBAxA3EDkQPhBJEFIQYBBkEGsQdBB5EIYQiRCWEJsQoxCmELgQuxDAAAAAAAAA\n\tAgEAAAAAAAAALQAAAAAAAAAAAAAAAAAAEMI=\n\t</data>\n\t<key>CursorColor</key>\n\t<data>\n\tYnBsaXN0MDDUAQIDBAUGFRZYJHZlcnNpb25YJG9iamVjdHNZJGFyY2hpdmVyVCR0b3AS\n\tAAGGoKMHCA9VJG51bGzTCQoLDA0OV05TV2hpdGVcTlNDb2xvclNwYWNlViRjbGFzc0sw\n\tLjMwMjQxOTM2ABADgALSEBESE1okY2xhc3NuYW1lWCRjbGFzc2VzV05TQ29sb3KiEhRY\n\tTlNPYmplY3RfEA9OU0tleWVkQXJjaGl2ZXLRFxhUcm9vdIABCBEaIy0yNztBSFBdZHBy\n\tdHmEjZWYobO2uwAAAAAAAAEBAAAAAAAAABkAAAAAAAAAAAAAAAAAAAC9\n\t</data>\n\t<key>Font</key>\n\t<data>\n\tYnBsaXN0MDDUAQIDBAUGGBlYJHZlcnNpb25YJG9iamVjdHNZJGFyY2hpdmVyVCR0b3AS\n\tAAGGoKQHCBESVSRudWxs1AkKCwwNDg8QVk5TU2l6ZVhOU2ZGbGFnc1ZOU05hbWVWJGNs\n\tYXNzI0AoAAAAAAAAEBCAAoADXU1lbmxvLVJlZ3VsYXLSExQVFlokY2xhc3NuYW1lWCRj\n\tbGFzc2VzVk5TRm9udKIVF1hOU09iamVjdF8QD05TS2V5ZWRBcmNoaXZlctEaG1Ryb290\n\tgAEIERojLTI3PEJLUltiaXJ0dniGi5afpqmyxMfMAAAAAAAAAQEAAAAAAAAAHAAAAAAA\n\tAAAAAAAAAAAAAM4=\n\t</data>\n\t<key>FontAntialias</key>\n\t<true/>\n\t<key>FontWidthSpacing</key>\n\t<real>0.99596774193548387</real>\n\t<key>ProfileCurrentVersion</key>\n\t<real>2.0499999999999998</real>\n\t<key>SelectionColor</key>\n\t<data>\n\tYnBsaXN0MDDUAQIDBAUGFRZYJHZlcnNpb25YJG9iamVjdHNZJGFyY2hpdmVyVCR0b3AS\n\tAAGGoKMHCA9VJG51bGzTCQoLDA0OV05TV2hpdGVcTlNDb2xvclNwYWNlViRjbGFzc0sw\n\tLjI1NDAzMjI1ABADgALSEBESE1okY2xhc3NuYW1lWCRjbGFzc2VzV05TQ29sb3KiEhRY\n\tTlNPYmplY3RfEA9OU0tleWVkQXJjaGl2ZXLRFxhUcm9vdIABCBEaIy0yNztBSFBdZHBy\n\tdHmEjZWYobO2uwAAAAAAAAEBAAAAAAAAABkAAAAAAAAAAAAAAAAAAAC9\n\t</data>\n\t<key>ShowWindowSettingsNameInTitle</key>\n\t<false/>\n\t<key>TextBoldColor</key>\n\t<data>\n\tYnBsaXN0MDDUAQIDBAUGFRZYJHZlcnNpb25YJG9iamVjdHNZJGFyY2hpdmVyVCR0b3AS\n\tAAGGoKMHCA9VJG51bGzTCQoLDA0OV05TV2hpdGVcTlNDb2xvclNwYWNlViRjbGFzc0Ix\n\tABADgALSEBESE1okY2xhc3NuYW1lWCRjbGFzc2VzV05TQ29sb3KiEhRYTlNPYmplY3Rf\n\tEA9OU0tleWVkQXJjaGl2ZXLRFxhUcm9vdIABCBEaIy0yNztBSFBdZGdpa3B7hIyPmKqt\n\tsgAAAAAAAAEBAAAAAAAAABkAAAAAAAAAAAAAAAAAAAC0\n\t</data>\n\t<key>TextColor</key>\n\t<data>\n\tYnBsaXN0MDDUAQIDBAUGKSpYJHZlcnNpb25YJG9iamVjdHNZJGFyY2hpdmVyVCR0b3AS\n\tAAGGoKcHCBMXGyImVSRudWxs1QkKCwwNDg8QERJcTlNDb21wb25lbnRzVU5TUkdCXE5T\n\tQ29sb3JTcGFjZV8QEk5TQ3VzdG9tQ29sb3JTcGFjZVYkY2xhc3NPECgwLjIzOTIxNTY4\n\tNjkgMC41MDk4MDM5NTA4IDAuNTUyOTQxMjAzMSAxTxAoMC4wOTA5NTIxMTMyNyAwLjQ0\n\tNDkyMDcxODcgMC40ODY2NTcyNjE4ABABgAKABtIUDRUWVU5TSUNDgAOABdIYDRkaV05T\n\tLmRhdGFPEQ8wAAAPMGFwcGwCEAAAbW50clJHQiBYWVogB+IABgAWAAsABQAeYWNzcEFQ\n\tUEwAAAAAQVBQTAAAAAAAAAAAAAAAAAAAAAAAAPbWAAEAAAAA0y1hcHBsAAAAAAAAAAAA\n\tAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARZGVzYwAAAVAAAABi\n\tZHNjbQAAAbQAAAQYY3BydAAABcwAAAAjd3RwdAAABfAAAAAUclhZWgAABgQAAAAUZ1hZ\n\tWgAABhgAAAAUYlhZWgAABiwAAAAUclRSQwAABkAAAAgMYWFyZwAADkwAAAAgdmNndAAA\n\tDmwAAAAwbmRpbgAADpwAAAA+Y2hhZAAADtwAAAAsbW1vZAAADwgAAAAoYlRSQwAABkAA\n\tAAgMZ1RSQwAABkAAAAgMYWFiZwAADkwAAAAgYWFnZwAADkwAAAAgZGVzYwAAAAAAAAAI\n\tRGlzcGxheQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\tAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG1sdWMAAAAAAAAAIgAA\n\tAAxockhSAAAAFAAAAahrb0tSAAAADAAAAbxuYk5PAAAAEgAAAchpZAAAAAAAEgAAAdpo\n\tdUhVAAAAFAAAAexjc0NaAAAAFgAAAgBkYURLAAAAHAAAAhZ1a1VBAAAAHAAAAjJhcgAA\n\tAAAAFAAAAk5pdElUAAAAFAAAAmJyb1JPAAAAEgAAAnZubE5MAAAAFgAAAohoZUlMAAAA\n\tFgAAAp5lc0VTAAAAEgAAAnZmaUZJAAAAEAAAArR6aFRXAAAADAAAAsR2aVZOAAAADgAA\n\tAtBza1NLAAAAFgAAAt56aENOAAAADAAAAsRydVJVAAAAJAAAAvRmckZSAAAAFgAAAxht\n\tcwAAAAAAEgAAAy5jYUVTAAAAGAAAA0B0aFRIAAAADAAAA1hlc1hMAAAAEgAAAnZkZURF\n\tAAAAEAAAA2RlblVTAAAAEgAAA3RwdEJSAAAAGAAAA4ZwbFBMAAAAEgAAA55lbEdSAAAA\n\tIgAAA7BzdlNFAAAAEAAAA9J0clRSAAAAFAAAA+JqYUpQAAAADAAAA/ZwdFBUAAAAFgAA\n\tBAIATABDAEQAIAB1ACAAYgBvAGoAac7st+wAIABMAEMARABGAGEAcgBnAGUALQBMAEMA\n\tRABMAEMARAAgAFcAYQByAG4AYQBTAHoA7QBuAGUAcwAgAEwAQwBEAEIAYQByAGUAdgBu\n\tAP0AIABMAEMARABMAEMARAAtAGYAYQByAHYAZQBzAGsA5gByAG0EGgQ+BDsETAQ+BEAE\n\tPgQyBDgEOQAgAEwAQwBEIA8ATABDAEQAIAZFBkQGSAZGBikATABDAEQAIABjAG8AbABv\n\tAHIAaQBMAEMARAAgAGMAbwBsAG8AcgBLAGwAZQB1AHIAZQBuAC0ATABDAEQgDwBMAEMA\n\tRAAgBeYF0QXiBdUF4AXZAFYA5AByAGkALQBMAEMARF9pgnIAIABMAEMARABMAEMARAAg\n\tAE0A4AB1AEYAYQByAGUAYgBuAP0AIABMAEMARAQmBDIENQRCBD0EPgQ5ACAEFgQaAC0E\n\tNAQ4BEEEPwQ7BDUEOQBMAEMARAAgAGMAbwB1AGwAZQB1AHIAVwBhAHIAbgBhACAATABD\n\tAEQATABDAEQAIABlAG4AIABjAG8AbABvAHIATABDAEQAIA4qDjUARgBhAHIAYgAtAEwA\n\tQwBEAEMAbwBsAG8AcgAgAEwAQwBEAEwAQwBEACAAQwBvAGwAbwByAGkAZABvAEsAbwBs\n\tAG8AcgAgAEwAQwBEA4gDswPHA8EDyQO8A7cAIAO/A7gDzAO9A7cAIABMAEMARABGAOQA\n\tcgBnAC0ATABDAEQAUgBlAG4AawBsAGkAIABMAEMARDCrMOkw/ABMAEMARABMAEMARAAg\n\tAGEAIABDAG8AcgBlAHN0ZXh0AAAAAENvcHlyaWdodCBBcHBsZSBJbmMuLCAyMDE4AABY\n\tWVogAAAAAAAA8xYAAQAAAAEWylhZWiAAAAAAAACDhwAAPan///+7WFlaIAAAAAAAAEvl\n\tAACz7wAACt1YWVogAAAAAAAAJ2oAAA5oAADIlWN1cnYAAAAAAAAEAAAAAAUACgAPABQA\n\tGQAeACMAKAAtADIANgA7AEAARQBKAE8AVABZAF4AYwBoAG0AcgB3AHwAgQCGAIsAkACV\n\tAJoAnwCjAKgArQCyALcAvADBAMYAywDQANUA2wDgAOUA6wDwAPYA+wEBAQcBDQETARkB\n\tHwElASsBMgE4AT4BRQFMAVIBWQFgAWcBbgF1AXwBgwGLAZIBmgGhAakBsQG5AcEByQHR\n\tAdkB4QHpAfIB+gIDAgwCFAIdAiYCLwI4AkECSwJUAl0CZwJxAnoChAKOApgCogKsArYC\n\twQLLAtUC4ALrAvUDAAMLAxYDIQMtAzgDQwNPA1oDZgNyA34DigOWA6IDrgO6A8cD0wPg\n\tA+wD+QQGBBMEIAQtBDsESARVBGMEcQR+BIwEmgSoBLYExATTBOEE8AT+BQ0FHAUrBToF\n\tSQVYBWcFdwWGBZYFpgW1BcUF1QXlBfYGBgYWBicGNwZIBlkGagZ7BowGnQavBsAG0Qbj\n\tBvUHBwcZBysHPQdPB2EHdAeGB5kHrAe/B9IH5Qf4CAsIHwgyCEYIWghuCIIIlgiqCL4I\n\t0gjnCPsJEAklCToJTwlkCXkJjwmkCboJzwnlCfsKEQonCj0KVApqCoEKmAquCsUK3Arz\n\tCwsLIgs5C1ELaQuAC5gLsAvIC+EL+QwSDCoMQwxcDHUMjgynDMAM2QzzDQ0NJg1ADVoN\n\tdA2ODakNww3eDfgOEw4uDkkOZA5/DpsOtg7SDu4PCQ8lD0EPXg96D5YPsw/PD+wQCRAm\n\tEEMQYRB+EJsQuRDXEPURExExEU8RbRGMEaoRyRHoEgcSJhJFEmQShBKjEsMS4xMDEyMT\n\tQxNjE4MTpBPFE+UUBhQnFEkUahSLFK0UzhTwFRIVNBVWFXgVmxW9FeAWAxYmFkkWbBaP\n\tFrIW1hb6Fx0XQRdlF4kXrhfSF/cYGxhAGGUYihivGNUY+hkgGUUZaxmRGbcZ3RoEGioa\n\tURp3Gp4axRrsGxQbOxtjG4obshvaHAIcKhxSHHscoxzMHPUdHh1HHXAdmR3DHeweFh5A\n\tHmoelB6+HukfEx8+H2kflB+/H+ogFSBBIGwgmCDEIPAhHCFIIXUhoSHOIfsiJyJVIoIi\n\tryLdIwojOCNmI5QjwiPwJB8kTSR8JKsk2iUJJTglaCWXJccl9yYnJlcmhya3JugnGCdJ\n\tJ3onqyfcKA0oPyhxKKIo1CkGKTgpaymdKdAqAio1KmgqmyrPKwIrNitpK50r0SwFLDks\n\tbiyiLNctDC1BLXYtqy3hLhYuTC6CLrcu7i8kL1ovkS/HL/4wNTBsMKQw2zESMUoxgjG6\n\tMfIyKjJjMpsy1DMNM0YzfzO4M/E0KzRlNJ402DUTNU01hzXCNf02NzZyNq426TckN2A3\n\tnDfXOBQ4UDiMOMg5BTlCOX85vDn5OjY6dDqyOu87LTtrO6o76DwnPGU8pDzjPSI9YT2h\n\tPeA+ID5gPqA+4D8hP2E/oj/iQCNAZECmQOdBKUFqQaxB7kIwQnJCtUL3QzpDfUPARANE\n\tR0SKRM5FEkVVRZpF3kYiRmdGq0bwRzVHe0fASAVIS0iRSNdJHUljSalJ8Eo3Sn1KxEsM\n\tS1NLmkviTCpMcky6TQJNSk2TTdxOJU5uTrdPAE9JT5NP3VAnUHFQu1EGUVBRm1HmUjFS\n\tfFLHUxNTX1OqU/ZUQlSPVNtVKFV1VcJWD1ZcVqlW91dEV5JX4FgvWH1Yy1kaWWlZuFoH\n\tWlZaplr1W0VblVvlXDVchlzWXSddeF3JXhpebF69Xw9fYV+zYAVgV2CqYPxhT2GiYfVi\n\tSWKcYvBjQ2OXY+tkQGSUZOllPWWSZedmPWaSZuhnPWeTZ+loP2iWaOxpQ2maafFqSGqf\n\tavdrT2una/9sV2yvbQhtYG25bhJua27Ebx5veG/RcCtwhnDgcTpxlXHwcktypnMBc11z\n\tuHQUdHB0zHUodYV14XY+dpt2+HdWd7N4EXhueMx5KnmJeed6RnqlewR7Y3vCfCF8gXzh\n\tfUF9oX4BfmJ+wn8jf4R/5YBHgKiBCoFrgc2CMIKSgvSDV4O6hB2EgITjhUeFq4YOhnKG\n\t14c7h5+IBIhpiM6JM4mZif6KZIrKizCLlov8jGOMyo0xjZiN/45mjs6PNo+ekAaQbpDW\n\tkT+RqJIRknqS45NNk7aUIJSKlPSVX5XJljSWn5cKl3WX4JhMmLiZJJmQmfyaaJrVm0Kb\n\tr5wcnImc951kndKeQJ6unx2fi5/6oGmg2KFHobaiJqKWowajdqPmpFakx6U4pammGqaL\n\tpv2nbqfgqFKoxKk3qamqHKqPqwKrdavprFys0K1ErbiuLa6hrxavi7AAsHWw6rFgsday\n\tS7LCszizrrQltJy1E7WKtgG2ebbwt2i34LhZuNG5SrnCuju6tbsuu6e8IbybvRW9j74K\n\tvoS+/796v/XAcMDswWfB48JfwtvDWMPUxFHEzsVLxcjGRsbDx0HHv8g9yLzJOsm5yjjK\n\tt8s2y7bMNcy1zTXNtc42zrbPN8+40DnQutE80b7SP9LB00TTxtRJ1MvVTtXR1lXW2Ndc\n\t1+DYZNjo2WzZ8dp22vvbgNwF3IrdEN2W3hzeot8p36/gNuC94UThzOJT4tvjY+Pr5HPk\n\t/OWE5g3mlucf56noMui86Ubp0Opb6uXrcOv77IbtEe2c7ijutO9A78zwWPDl8XLx//KM\n\t8xnzp/Q09ML1UPXe9m32+/eK+Bn4qPk4+cf6V/rn+3f8B/yY/Sn9uv5L/tz/bf//cGFy\n\tYQAAAAAAAwAAAAJmZgAA8qcAAA1ZAAAT0AAACg52Y2d0AAAAAAAAAAEAAQAAAAAAAAAB\n\tAAAAAQAAAAAAAAABAAAAAQAAAAAAAAABAABuZGluAAAAAAAAADYAAK4AAABSAAAAQ8AA\n\tALDAAAAmQAAADYAAAFAAAABUQAACMzMAAjMzAAIzMwAAAAAAAAAAc2YzMgAAAAAAAQxy\n\tAAAF+P//8x0AAAe6AAD9cv//+53///2kAAAD2QAAwHFtbW9kAAAAAAAABhAAAKAwAAAA\n\tANIfswAAAAAAAAAAAAAAAAAAAAAAgATSHB0eH1okY2xhc3NuYW1lWCRjbGFzc2VzXU5T\n\tTXV0YWJsZURhdGGjHiAhVk5TRGF0YVhOU09iamVjdNIcHSMkXE5TQ29sb3JTcGFjZaIl\n\tIVxOU0NvbG9yU3BhY2XSHB0nKFdOU0NvbG9yoichXxAPTlNLZXllZEFyY2hpdmVy0Sss\n\tVHJvb3SAAQAIABEAGgAjAC0AMgA3AD8ARQBQAF0AYwBwAIUAjAC3AOIA5ADmAOgA7QDz\n\tAPUA9wD8AQQQOBA6ED8QShBTEGEQZRBsEHUQehCHEIoQlxCcEKQQpxC5ELwQwQAAAAAA\n\tAAIBAAAAAAAAAC0AAAAAAAAAAAAAAAAAABDD\n\t</data>\n\t<key>columnCount</key>\n\t<integer>180</integer>\n\t<key>name</key>\n\t<string>tmp</string>\n\t<key>rowCount</key>\n\t<integer>35</integer>\n\t<key>shellExitAction</key>\n\t<integer>2</integer>\n\t<key>type</key>\n\t<string>Window Settings</string>\n</dict>\n</plist>\n'
    OSA("Terminal", ["cmd_n", "delay 1"])
  def shrink(self):
    app = OSA().getforemostwindowapp()
    OSA().setforemostwindowarrangement(app, 0, 0, 35, 35)
class Psutil(DecisionTree):
  def tests(self):
    builtin_print(        "net_connections #1: %s" % str(self.net_connections()[0])                                   )
    builtin_print(        "net_io_counters: %s" % str(self.net_io_counters())                                         )
    builtin_print(        "sensors_battery: %s" % str(self.sensors_battery())                                         )
    builtin_print(        "boot_time: %s" % str(self.boot_time())                                                     )
    builtin_print(        "virtual_memory: %s" % str(self.virtual_memory())                                           )
    builtin_print(        "cpu_count: %s" % str(self.cpu_count())                                                     )
    builtin_print(        "disk_partitions: %s" % str(self.disk_partitions())                                         )
    builtin_print(        "disk_usage: %s" % str(self.disk_usage())                                                   )
    builtin_print(        "GetHumanReadable: %s" % str(self.GetHumanReadable(self.disk_usage().total))                )
  def get_network_interface(self):
    x = subprocess.getoutput("route get 10.10.10.10")
    redprint("route get 10.10.10.10\n==RESULT==\n\n{}\n\n".format(x))
    return re.findall(r"interface: (.*)", x)[0]
  def get_mac_lan_ip_address(self):
    w = "ipconfig getifaddr {}".format(self.get_network_interface())
    x = subprocess.getoutput(w)
    redprint("{}\n==RESULT==\n\n{}\n\n".format(w,x))
    return x
  def nmap(self):
    w = "sudo nmap -sP {}.1/24".format(Join(".",self.get_mac_lan_ip_address().split(".")[:3]))
    x = subprocess.getoutput(w)
    z = re.findall(r"Nmap scan report for (.*) .*\((.*)\)",x)
    redprint("{}\n==result\n\n{}\n\n{}\n\n".format(w,x,json.dumps(z,indent=4)))
    return z
  def nonsudo_nmap(self):
    w = "nmap -sP {}.1/24".format(Join(".",self.get_mac_lan_ip_address().split(".")[:3]))
    x = subprocess.getoutput(w)
    z = re.findall(r"Nmap scan report for (.*) .*\((.*)\)",x)
    redprint("{}\n==result\n\n{}\n\n{}\n\n".format(w,x,json.dumps(z,indent=4)))
    return z
  def nmap_consistent(self,c=1):
    while True:
      if(len(self.nonsudo_nmap())) != c:
        OSA().notify("lol")
  def net_connections(self):
    return psutil.net_connections(kind='inet')
  def net_io_counters(self):
    return psutil.net_io_counters(pernic=False, nowrap=True)
  def sensors_battery(self):
    return psutil.sensors_battery()
  def boot_time(self):
    psutil.boot_time()
    import datetime
    datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    """ '2018-08-29 04:23:28' """
  def virtual_memory(self):
    mem = psutil.virtual_memory()
    return mem
  def cpu_count(self):
    return psutil.cpu_count()
    """ 8 """
  def disk_partitions(self):
    return psutil.disk_partitions()
  def disk_usage(self):
    return psutil.disk_usage("/")
  @staticmethod
  def GetMachineReadable(HumanReadable):
    suffixes=['B','KB','MB','GB','TB']
    x = int(re.findall("[0-9]+",HumanReadable)[0])
    y = re.findall(r"[a-zA-Z]+",HumanReadable)[0]
    z = suffixes.index(y)
    for i in range(z):
      x = x*1024
    return x
  @staticmethod
  def GetHumanReadable(size,precision=2):
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
      suffixIndex += 1 #increment the index of the suffix
      size = size/1024.0 #apply the division
    return "%.*f%s"%(precision,size,suffixes[suffixIndex])
  def GetLetterReadable(self,v):
    return v if v<= 999 else(str(int(v/1000)) + "K")if(1000 <= v <= 999999)else(str(int(v/1000000)) + "M")if(1000000 <= v <= 999999999)else(str(int(v/1000000000)) + "B")if(1000000000 <= v <= 999999999999)else("?")
    """ tests """
    for i in [0,999,1000,50000,500000,5000000,5000000000,50000000,50000000000,5000000000000,6456498098,123491823,123123]:
      print(x(i))
  def SpeedTest(self, download = True, upload = True, verbose = True):
    start_time = datetime.now()

    import speedtest

    servers = []
    # If you want to test against a specific server
    # servers = [1234]

    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    if download == True:
      s.download()
    if upload == True:
      s.upload()
    s.results.share()

    results_dict = s.results.dict()
    results_dict = AttrDict(results_dict)

    end_time = datetime.now()
    elapsed_time = end_time.__sub__(start_time)
    elapsed_time_seconds = elapsed_time.seconds
    elapsed_time_microseconds = elapsed_time.microseconds / 1000000
    elapsed_time_full = elapsed_time_seconds + elapsed_time_microseconds
    elapsed_time_full = round(elapsed_time_full, 2)
    time.sleep(1)
    if verbose == True:
      greenprint("speed test results time taken: %s seconds" % elapsed_time_full)
    if verbose == True:
      greenprint("")
    time.sleep(1)
    if verbose == True:
      greenprint(":Results:")

    download_speed = None
    download_speed_readable = None
    if download == True:
      download_speed = results_dict.download
      download_speed_readable = Psutil().GetLetterReadable(download_speed)
      if verbose == True:
        greenprint("download speed: %s" % download_speed_readable)

    upload_speed = None
    upload_speed_readable = None
    if upload == True:
      upload_speed = results_dict.upload
      upload_speed_readable = Psutil().GetLetterReadable(upload_speed)
      if verbose == True:
        greenprint("upload speed: %s" % upload_speed_readable)

    if download == True and upload == True:
      return download_speed_readable, upload_speed_readable
    elif download == True and upload == False:
      return download_speed_readable
    elif download == False and upload == True:
      return upload_speed_readable
    else:
      return None
    """ :Test:
    results = []
    results.append(Psutil().SpeedTest(download = True, upload = True))
    results.append(Psutil().SpeedTest(download = True, upload = False))
    results.append(Psutil().SpeedTest(download = False, upload = True))
    results.append(Psutil().SpeedTest(download = False, upload = False))
    assert len(results[0]) == 2
    assert results[1]
    assert results[2]
    assert results[3] == None
    greenprint(results)
    """
class SublimeText_Themes(DecisionTree):
  # (cbf52c (24bc44))
  # (9c8996 (ffffff))
  def __init__(self, ):
    self.hexes = []
    print(" a nice app: http://tmtheme-editor.herokuapp.com/#!/editor/theme/Monokai")
    self.functions_sorted = ["normal", "change_colours", "change_comment_colours", "colorama", "change_background_colour"]
    self.discovered_colours = {
                                "teal": "00efaf",
                                "darkteal": "00afaf", }
    self.saved_colour_codes = """
                                  66D9EF
                                  00qfaf
                                  b7e88a # a fun green
                                  3b3d60
                                  c95e46
                                  b6af6c
                                  502846
                                  51c56d
                                  24bc44
                                  a9586a
                                  c1ef4e
                                  c58887
                                  188711
                                  395931 # a nice calm sea green
                                  9d8bcc
                                  83bd5a
                                  e63f57
                                  e343f0
                                  71321a
                                  395931
                                  2a281a
                                  ef6978
                                  02f718 # sharp green
                                  9c8996 # purplish
                                  d4d4ae #
                                  efd2b4 # pinkish
                                  b3e7b2 #
                                  a5ccd7 #
                                  ffffff # white 
                                  db7d5a # sandstone aurauric red
                                  1ebd01 # in the cut green
                                  ff1700 # red
                                  b00e2a # funner red
                                  ebfdb4 # a surreal colour
                                  cbf52c # a stay awake green and yellow
                                  4fe1e5 # mega blue
                                  deeabd # draconian white
                                  c1faea # funny room blue
                                  efc98e # desaddening orange
                                  6f7f84 #                                  
                                  d6ddd5 2bfe16
                                  dbf0f7 3ecefb
                                  96f6ce d97462
                                  f55608 bfaafe
                                  d48ee5 0ecb9f
                                  748054 fe3161
                                  e04023 befbf6
                                  af53f4 6d7d31
                                  f59b00 de1939
                                  78a7b2 400939"""
    list(map(print, self.saved_colour_codes.split("\n")))
    self.theme_path = userfolder("~/Library/Application Support/Sublime Text 3/Packages/Color Scheme - Default/Monokai.tmTheme")
    self.blank = '\n          <!-- \x01 Maybe strings should be whitetext \x02 Functions purple? \x03 Variables blue? \x04 Numbers green? \x05 what about a very dark green for functions?-->\n          <?xml version="1.0" encoding="UTF-8"?>\n          <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n          <plist version="1.0">\n          <dict>\n            <key>name</key>\n            <string>Monokai</string>\n            <key>settings</key>\n            <array>\n              <dict>\n                <key>settings</key>\n                <!--\n                  [[ Original Data ]]\n                <dict>\n                  <key>background</key>\n                  <string>#__blank__</string> \n                  <key>caret</key>\n                  <string>#__blank__</string>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                  <key>invisibles</key>\n                  <string>#__blank__</string>\n                  <key>lineHighlight</key>\n                  <string>#__blank__</string>\n                  <key>selection</key>\n                  <string>#__blank__</string>\n                  <key>findHighlight</key>\n                  <string>#__blank__</string>\n                  <key>findHighlightForeground</key>\n                  <string>#__blank__</string>\n                  <key>selectionBorder</key>\n                  <string>#__blank__</string>\n                  <key>activeGuide</key>\n                  <string>#__blank__</string>\n                  <key>misspelling</key>\n                  <string>#__blank__</string>\n                  <key>bracketsForeground</key>\n                  <string>#__blank__</string>\n                  <key>bracketsOptions</key>\n                  <string>underline</string>\n                  <key>bracketContentsForeground</key>\n                  <string>#__blank__</string>\n                  <key>bracketContentsOptions</key>\n                  <string>underline</string>\n                  <key>tagsOptions</key>\n                  <string>stippled_underline</string>\n                </dict>\n                -->\n                <!--\n                https://html-color-codes.info/old/colorpicker.html\n                -->\n                <dict>\n                  <key>background</key>\n                  <string>#000000</string>\n                  <key>caret</key>\n                  <string>#__blank__</string>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                  <key>invisibles</key>\n                  <string>#__blank__</string>\n                  <key>lineHighlight</key>\n                  <string>#__blank__</string>\n                  <key>selection</key>\n                  <string>#000000</string>\n                  <key>findHighlight</key>\n                  <string>#__blank__</string>\n                  <key>findHighlightForeground</key>\n                  <string>#__blank__</string>\n                  <key>selectionBorder</key>\n                  <string>#__blank__</string>\n                  <key>activeGuide</key>\n                  <string>#__blank__</string>\n                  <key>misspelling</key>\n                  <string>#__blank__</string>\n                  <key>bracketsForeground</key>\n                  <string>#__blank__</string>\n                  <key>bracketsOptions</key>\n                  <string>underline</string>\n                  <key>bracketContentsForeground</key>\n                  <string>#__blank__</string>\n                  <key>bracketContentsOptions</key>\n                  <string>underline</string>\n                  <key>tagsOptions</key>\n                  <string>stippled_underline</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Comment</string>\n                <key>scope</key>\n                <string>comment</string>\n                <key>settings</key>\n                <!--\n                [[ Original Data ]]\n                <dict>\n                  <key>foreground</key>\n                  <string>#{__blank__}</string>\n                </dict>\n                -->\n                <dict>\n                  <key>foreground</key>\n                  <string>#FF1700</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>String</string>\n                <key>scope</key>\n                <string>string</string>\n                <key>settings</key>\n                <!--\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n                -->\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string> <!--"string here" # __blank__ string-->\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Number</string>\n                <key>scope</key>\n                <string>constant.numeric</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n\n              <dict>\n                <key>name</key>\n                <string>Built-in constant</string>\n                <key>scope</key>\n                <string>constant.language</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string> <!-- while (True)-->\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>User-defined constant</string>\n                <key>scope</key>\n                <string>constant.character, constant.other</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string> <!-- %s -->\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Variable</string>\n                <key>scope</key>\n                <string>variable</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string></string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Keyword</string>\n                <key>scope</key>\n                <string>keyword - (source.c keyword.operator | source.c++ keyword.operator | source.objc keyword.operator | source.objc++ keyword.operator), keyword.operator.word</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string> <!-- default #__blank__ import/while/for/try/except/as -->\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Annotation Punctuation</string>\n                <key>scope</key>\n                <string>punctuation.definition.annotation</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>JavaScript Dollar</string>\n                <key>scope</key>\n                <string>variable.other.dollar.only.js</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Storage</string>\n                <key>scope</key>\n                <string>storage</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string></string>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Storage type</string>\n                <key>scope</key>\n                <string>storage.type</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string>italic</string>\n                  <key>foreground</key>\n                  <string>#__blank__</string> <!-- default: __blank__ (class/def) -->\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Entity name</string>\n                <key>scope</key>\n                <string>entity.name - (entity.name.filename | entity.name.section | entity.name.tag | entity.name.label)</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string></string>\n                  <key>foreground</key>\n                  <string>#__blank__</string> <!-- default: A6E22E class/def (function)-->\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Inherited class</string>\n                <key>scope</key>\n                <string>entity.other.inherited-class</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string>italic underline</string>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Function argument</string>\n                <key>scope</key>\n                <string>variable.parameter - (source.c | source.c++ | source.objc | source.objc++)</string>\n                <key>settings</key>\n                <!--\n                <dict>\n                  <key>fontStyle</key>\n                  <string>italic</string>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n                -->\n                <dict>\n                  <key>fontStyle</key>\n                  <string>italic</string>\n                  <key>foreground</key>\n                  <string>#__blank__</string> <!-- def hi( (kw)= ) -->\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Language variable</string>\n                <key>scope</key>\n                <string>variable.language</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string>italic</string>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Tag name</string>\n                <key>scope</key>\n                <string>entity.name.tag</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string></string>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Tag attribute</string>\n                <key>scope</key>\n                <string>entity.other.attribute-name</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string></string>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Function call</string>\n                <key>scope</key>\n                <string>variable.function, variable.annotation</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string></string>\n                  <key>foreground</key>\n                  <string>#__blank__</string> <!--x.stdout.readline()) (readline()) -->\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Library function</string> <!--input("Product_url?: ") #__blank__-->\n                <key>scope</key>\n                <string>support.function, support.macro</string>\n                <key>settings</key>\n                <!--\n                <dict>\n                  <key>fontStyle</key>\n                  <string></string>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n                -->\n                <dict>\n                  <key>fontStyle</key>\n                  <string></string>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Library constant</string>\n                <key>scope</key>\n                <string>support.constant</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string></string>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Library class/type</string>\n                <key>scope</key>\n                <string>support.type, support.class</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string>italic</string>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Library variable</string>\n                <key>scope</key>\n                <string>support.other.variable</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string></string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Invalid</string>\n                <key>scope</key>\n                <string>invalid</string>\n                <key>settings</key>\n                <dict>\n                  <key>background</key>\n                  <string>#000000</string>\n                  <key>fontStyle</key>\n                  <string></string>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>Invalid deprecated</string>\n                <key>scope</key>\n                <string>invalid.deprecated</string>\n                <key>settings</key>\n                <dict>\n                  <key>background</key>\n                  <string>#__blank__</string>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>JSON String</string>\n                <key>scope</key>\n                <string>meta.structure.dictionary.json string.quoted.double.json</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>YAML String</string>\n                <key>scope</key>\n                <string>string.unquoted.yaml</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n\n              <dict>\n                <key>name</key>\n                <string>diff.header</string>\n                <key>scope</key>\n                <string>meta.diff, meta.diff.header</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>markup headings</string>\n                <key>scope</key>\n                <string>markup.heading</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string>bold</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>markup headings</string>\n                <key>scope</key>\n                <string>markup.heading punctuation.definition.heading</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>markup h1</string>\n                <key>scope</key>\n                <string>markup.heading.1 punctuation.definition.heading</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>markup links</string>\n                <key>scope</key>\n                <string>markup.underline.link</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>markup bold</string>\n                <key>scope</key>\n                <string>markup.bold</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string>bold</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>markup italic</string>\n                <key>scope</key>\n                <string>markup.italic</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string>italic</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>markup bold/italic</string>\n                <key>scope</key>\n                <string>markup.italic markup.bold | markup.bold markup.italic</string>\n                <key>settings</key>\n                <dict>\n                  <key>fontStyle</key>\n                  <string>bold italic</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>markup hr</string>\n                <key>scope</key>\n                <string>punctuation.definition.thematic-break</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>markup blockquote</string>\n                <key>scope</key>\n                <string>markup.quote punctuation.definition.blockquote</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>markup bullets</string>\n                <key>scope</key>\n                <string>markup.list.numbered.bullet</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>markup bullets</string>\n                <key>scope</key>\n                <string>markup.list.unnumbered.bullet | (markup.list.numbered punctuation.definition)</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>markup code</string>\n                <key>scope</key>\n                <string>markup.raw</string>\n                <key>settings</key>\n                <dict>\n                  <key>background</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>markup punctuation</string>\n                <key>scope</key>\n                <string>markup.raw punctuation.definition.raw</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>markup punctuation</string>\n                <key>scope</key>\n                <string>text &amp; (punctuation.definition.italic | punctuation.definition.bold | punctuation.definition.raw | punctuation.definition.link | punctuation.definition.metadata | punctuation.definition.image | punctuation.separator.table-cell | punctuation.section.table-header | punctuation.definition.constant)</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>diff.deleted</string>\n                <key>scope</key>\n                <string>markup.deleted</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>diff.inserted</string>\n                <key>scope</key>\n                <string>markup.inserted</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>name</key>\n                <string>diff.changed</string>\n                <key>scope</key>\n                <string>markup.changed</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>scope</key>\n                <string>constant.numeric.line-number.find-in-files - match</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n              <dict>\n                <key>scope</key>\n                <string>entity.name.filename</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n\n              <dict>\n                <key>scope</key>\n                <string>message.error</string>\n                <key>settings</key>\n                <dict>\n                  <key>foreground</key>\n                  <string>#__blank__</string>\n                </dict>\n              </dict>\n            </array>\n          </dict>\n          </plist>'
    self.Monokai_color_scheme = '{\n    "name": "Monokai",\n    "author": "Sublime HQ Pty Ltd, Wimer Hazenberg",\n    "variables":\n    {\n        "text": "#ffffff",\n        "background": "#000000",\n        "comment": "#ff1700",\n    },\n    "globals":\n    {\n        "foreground": "var(text)",\n        "background": "var(background)",\n        "caret": "var(text)",\n        "invisibles": "var(background)",\n        "line_highlight": "var(background)",\n        "selection": "var(background)",\n        "selection_border": "var(text)",\n        "misspelling": "var(background)",\n        "active_guide": "var(text)",\n        "find_highlight_foreground": "var(text)",\n        "find_highlight": "var(text)",\n        "brackets_options": "underline",\n        "brackets_foreground": "var(text)",\n        "bracket_contents_options": "underline",\n        "bracket_contents_foreground": "var(text)",\n        "tags_options": "stippled_underline"\n    },    "rules":\n    [\n        {\n            "name": "Comment",\n            "scope": "comment",\n            "foreground": "var(comment)"\n        },\n        {\n            "name": "String",\n            "scope": "string",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "Number",\n            "scope": "constant.numeric",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "Built-in constant",\n            "scope": "constant.language",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "User-defined constant",\n            "scope": "constant.character, constant.other",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "Variable",\n            "scope": "variable"\n        },\n        {\n            "name": "Keyword",\n            "scope": "keyword - (source.c keyword.operator | source.c++ keyword.operator | source.objc keyword.operator | source.objc++ keyword.operator), keyword.operator.word",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "Annotation Punctuation",\n            "scope": "punctuation.definition.annotation",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "JavaScript Dollar",\n            "scope": "variable.other.dollar.only.js",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "Storage",\n            "scope": "storage",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "Storage type",\n            "scope": "storage.type",\n            "foreground": "var(text)",\n            "font_style": "italic"\n        },\n        {\n            "name": "Entity name",\n            "scope": "entity.name - (entity.name.filename | entity.name.section | entity.name.tag | entity.name.label)",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "Inherited class",\n            "scope": "entity.other.inherited-class",\n            "foreground": "var(text)",\n            "font_style": "italic underline"\n        },\n        {\n            "name": "Function argument",\n            "scope": "variable.parameter - (source.c | source.c++ | source.objc | source.objc++)",\n            "foreground": "var(text)",\n            "font_style": "italic"\n        },\n        {\n            "name": "Language variable",\n            "scope": "variable.language",\n            "foreground": "var(text)",\n            "font_style": "italic"\n        },\n        {\n            "name": "Tag name",\n            "scope": "entity.name.tag",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "Tag attribute",\n            "scope": "entity.other.attribute-name",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "Function call",\n            "scope": "variable.function, variable.annotation",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "Library function",\n            "scope": "support.function, support.macro",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "Library constant",\n            "scope": "support.constant",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "Library class/type",\n            "scope": "support.type, support.class",\n            "foreground": "var(text)",\n            "font_style": "italic"\n        },\n        {\n            "name": "Library variable",\n            "scope": "support.other.variable"\n        },\n        {\n            "name": "Invalid",\n            "scope": "invalid",\n            "foreground": "var(text)",\n            "background": "var(background)"\n        },\n        {\n            "name": "Invalid deprecated",\n            "scope": "invalid.deprecated",\n            "foreground": "var(text)",\n            "background": "var(background)"\n        },\n        {\n            "name": "JSON String",\n            "scope": "meta.structure.dictionary.json string.quoted.double.json",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "YAML String",\n            "scope": "string.unquoted.yaml",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "diff.header",\n            "scope": "meta.diff, meta.diff.header",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "markup headings",\n            "scope": "markup.heading",\n            "font_style": "bold"\n        },\n        {\n            "name": "markup headings",\n            "scope": "markup.heading punctuation.definition.heading",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "markup h1",\n            "scope": "markup.heading.1 punctuation.definition.heading",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "markup links",\n            "scope": "markup.underline.link",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "markup bold",\n            "scope": "markup.bold",\n            "font_style": "bold"\n        },\n        {\n            "name": "markup italic",\n            "scope": "markup.italic",\n            "font_style": "italic"\n        },\n        {\n            "name": "markup bold/italic",\n            "scope": "markup.italic markup.bold | markup.bold markup.italic",\n            "font_style": "bold italic"\n        },\n        {\n            "name": "markup hr",\n            "scope": "punctuation.definition.thematic-break",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "markup blockquote",\n            "scope": "markup.quote punctuation.definition.blockquote",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "markup bullets",\n            "scope": "markup.list.numbered.bullet",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "markup bullets",\n            "scope": "markup.list.unnumbered.bullet | (markup.list.numbered punctuation.definition)",\n            "foreground": "color(var(text)"\n        },\n        {\n            "name": "markup code",\n            "scope": "markup.raw",\n            "background": "color(var(text)"\n        },\n        {\n            "name": "markup punctuation",\n            "scope": "markup.raw punctuation.definition.raw",\n            "foreground": "color(var(text)"\n        },\n        {\n            "name": "markup punctuation",\n            "scope": "text & (punctuation.definition.italic | punctuation.definition.bold | punctuation.definition.raw | punctuation.definition.link | punctuation.definition.metadata | punctuation.definition.image | punctuation.separator.table-cell | punctuation.section.table-header | punctuation.definition.constant)",\n            "foreground": "color(var(text)"\n        },\n        {\n            "name": "diff.deleted",\n            "scope": "markup.deleted",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "diff.inserted",\n            "scope": "markup.inserted",\n            "foreground": "var(text)"\n        },\n        {\n            "name": "diff.changed",\n            "scope": "markup.changed",\n            "foreground": "var(text)"\n        },\n        {\n            "scope": "constant.numeric.line-number.find-in-files - match",\n            "foreground": "color(var(text)"\n        },\n        {\n            "scope": "entity.name.filename",\n            "foreground": "var(text)"\n        },\n        {\n            "scope": "message.error",\n            "foreground": "var(text)"\n        }\n    ]\n}'
  def get_random_color_code(self):
    x = [0,1,2,3,4,5,6,7,8,9,"a","b","c","d","e","f"]
    import random
    y = ""
    for i in range(6):
      y += str(random.sample(x, 1)[0])
    print(y)
    return y
  def colorama(self, specific_colour_code = None, sleeptime=2):
    try:specific_colour_code = eval(specific_colour_code)
    except:pass
    if specific_colour_code == "on_clipboard":
      for idx, i in enumerate(pyperclip.paste().split("\n")):
        with open(self.theme_path, "w") as f:
          f.write(self.blank.replace("__blank__", i))
          os.system("say '%s'"%idx)
        time.sleep(int(sleeptime))
      return
    while True:
      with open(self.theme_path, "w") as f:
        if specific_colour_code == None:
          f.write(self.blank.replace("__blank__", self.get_random_color_code()))
        else:
          f.write(self.blank.replace("__blank__", specific_colour_code))
          return
      time.sleep(int(sleeptime))
  def change_colours(self, color_code = None):
    print(json.dumps(self.discovered_colours, indent=4))
    with open(self.theme_path, "w") as f:
      f.write(self.blank.replace("__blank__", color_code))
  def change_comment_colours(self, color_code = None):
    with open(self.theme_path, "r") as f:
      x = f.read()
    with open(self.theme_path, "w") as f:
      f.write(x.replace("FF1700", color_code))
  def change_background_colour(self, color_code = None):
    with open(self.theme_path, "r") as f:
      x = f.read()
    with open(self.theme_path, "w") as f:
      f.write(x.replace("000000", color_code))
  def normal(self):
    SublimeText_Normal_text = ExecutableText().export("SublimeText_Normal_text")
    with open(self.theme_path, "w") as f:
      f.write(SublimeText_Normal_text)
  def argh_text(self, hex="ffffff"):
    hex=(self.get_random_color_code())if(None==hex)else(hex)
    self.hexes[-1].argh_text = hex
    R = userfolder("~/Library/Application Support/Sublime Text 3/Packages/Color Scheme - Default/Monokai.sublime-color-scheme")
    F = re.sub(r'"text": "#.*', '"text": "#%s",' % (hex), open(R,"r").read())
    open(R, "w").write(F)
  def argh2_comments(self, hex="ffffff"):
    hex=(self.get_random_color_code())if(None==hex)else(hex)
    self.hexes[-1].argh2_comments = hex
    R = userfolder("~/Library/Application Support/Sublime Text 3/Packages/Color Scheme - Default/Monokai.sublime-color-scheme")
    F = re.sub(r'"comment": "#.*', '"comment": "#%s",' % (hex), open(R,"r").read())
    open(R, "w").write(F)
  def argh_background(self, hex="000000"):
    hex=(self.get_random_color_code())if(None==hex)else(hex)
    self.hexes[-1].argh_background = hex
    R = userfolder("~/Library/Application Support/Sublime Text 3/Packages/Color Scheme - Default/Monokai.sublime-color-scheme")
    F = re.sub(r'"background": "#.*', '"background": "#%s",' % (hex), open(R,"r").read())
    open(R, "w").write(F)
  def argh_colorama(self, text = True, comments = True, background = False, direction = None):
    if direction is not None:
      if direction == "left":
        self.current_idx = self.current_idx - 1 if (self.current_idx - 1) >= 0 else self.current_idx
        if text: self.argh_text(self.hexes[self.current_idx].argh_text)
        if comments: self.argh2_comments(self.hexes[self.current_idx].argh2_comments)
        if background: self.argh_background(self.hexes[self.current_idx].argh_background)
      elif direction == "right":
        self.current_idx = self.current_idx + 1 if (self.current_idx + 1) < len(self.hexes) else self.current_idx
        if text: self.argh_text(self.hexes[self.current_idx].argh_text)
        if comments: self.argh2_comments(self.hexes[self.current_idx].argh2_comments)
        if background: self.argh_background(self.hexes[self.current_idx].argh_background)
      return
    self.hexes.append(AttrDict())
    self.current_idx = len(self.hexes) - 1
    if text == True:
      self.argh_text(hex = None)
    elif text != False:
      self.argh_text(hex = text)

    if comments == True:
      self.argh2_comments(hex = None)
    elif comments != False:
      self.argh2_comments(hex = comments)

    if background == True:
      self.argh_background(hex = None)
    elif background != False:
      self.argh_background(hex = background)
      
  def argh_norm(self):
    R = userfolder("~/Library/Application Support/Sublime Text 3/Packages/Color Scheme - Default/Monokai.sublime-color-scheme")
    open(R, "w").write(self.Monokai_color_scheme)
class Url_Utils:
  def chromejs(x):
    blueprint("View -> Developer -> Allow JavaScript from Apple Events")
    x = 'tell application "Google Chrome 70" to execute front window\'s active tab javascript "%s"'%x
    fn = get_random_address(userfolder("~/tavern/tavern/soda/dls"))
    blueprint(fn)
    open(fn, "w").write(x)
    r = subprocess.getoutput("osascript %s"%fn)
    os.remove(fn)
    return r
    """
    x = "alert('example');"
    chromejs(x)
    """
  def getchromesource(r=None):
    redprint("Google Chrome -> View -> Developer -> Allow JavaScript from Apple Events")
    if r: r = check_output('osascript -e \'tell application "Google Chrome 70"\' -e "set source to execute tab %s of window 1 javascript \\"document.documentElement.outerHTML\\"" -e "end tell"'%(r))
    else: r = check_output('osascript -e \'tell application "Google Chrome 70"\' -e "set source to execute front window\'s active tab javascript \\"document.documentElement.outerHTML\\"" -e "end tell"')
    if "Google Chrome 70 got an error: Executing JavaScript through AppleScript is turned off." in r:
      # from http://hints.macworld.com/article.php?story=20060921045743404
      if OSA.display_dialog("Google Chrome 70 currently has Executing JavaScript through AppleScript turned off. Turn it on (it will be required for the program to work.)?",text_prompt=False,buttons=["Yes","No"]) == "No":
        return ""
      blueprint('tell application "Google Chrome 70"\n  activate\nend tell\ntell application "System Events"\n  tell process "Google Chrome"\n    tell menu bar 1\n      tell menu bar item "View"\n        tell menu "View"\n          tell menu item "Developer"\n            tell menu "Developer"\n              click menu item "Allow JavaScript from Apple Events"\n            end tell\n          end tell\n        end tell\n      end tell\n    end tell\n  end tell\nend tell')
      os.system("""osascript -e 'tell application "Google Chrome 70"' -e 'activate' -e 'end tell' -e 'tell application "System Events"' -e 'tell process "Google Chrome"' -e 'tell menu bar 1' -e 'tell menu bar item "View"' -e 'tell menu "View"' -e 'tell menu item "Developer"' -e 'tell menu "Developer"' -e 'click menu item "Allow JavaScript from Apple Events"' -e 'end tell' -e 'end tell' -e 'end tell' -e 'end tell' -e 'end tell' -e 'end tell' -e 'end tell'""")
      return getchromesource(r)
    return r
  def getsafarisource():
    blueprint("Safari -> Advanced -> Show develop menu ; Develop -> Allow JavaScript from Apple Events")
    x = subprocess.check_output("""osascript -e 'tell application "Safari" to set my_html to source of document 1'""",shell=True).decode("utf-8",errors="backslashreplace")
    return x
  def getsafariurl():
    x = subprocess.getoutput("""osascript -e 'tell application "Safari" to set the_url to URL of current tab of window 1'""")
    return x
  def get_all_chrome_urls():
    return subprocess.getoutput("""osascript -e'set text item delimiters to linefeed' -e'tell app "Google Chrome 70" to url of tabs of window 1 as text'""").split("\n")
  def get_first_chrome_url(q=None):
    x = None
    if q:
      v = pool(lambda i: subprocess.getoutput("""osascript -e 'tell application "Google Chrome 70" to get URL of active tab of window %s'"""%i),list(range(getwindowcount("Google Chrome 70")))).result()
      v = [i for i in v if q in i]
      assert len(v) == 1
      x = v[0]
    else:
      x = timed(lambda:subprocess.getoutput("""osascript -e 'tell application "Google Chrome 70" to get URL of active tab of first window'"""),5)
      if x == None:
        ()if(OSA.log("Can't get window. Have to end all Google Chrome processes and restart again. Click OK to continue. Clicking Abort will abort.",tp=False,buttons=["Abort","OK"])=="OK")else(0/0)
        os.system("killall Google\ Chrome")
        OSA.log("Please restart Google Chrome and navigate to the previous urls",tp=False)
        return get_first_chrome_url(q=q)
    # OSA.notify("got url: %s" % x)
    if "Not authorized to send Apple events to Google Chrome 70" in x:
      # from http://hints.macworld.com/article.php?story=20060921045743404
      if OSA.display_dialog("Google Chrome 70 currently has Executing JavaScript through AppleScript turned off. Turn it on (it will be required for the program to work.)?",text_prompt=False,buttons=["Yes","No"]) == "No":
        return ""
      os.system("""osascript -e 'tell application "Google Chrome 70"' -e 'activate' -e 'end tell' -e 'tell application "System Events"' -e 'tell process "Google Chrome"' -e 'tell menu bar 1' -e 'tell menu bar item "View"' -e 'tell menu "View"' -e 'tell menu item "Developer"' -e 'tell menu "Developer"' -e 'click menu item "Allow JavaScript from Apple Events"' -e 'end tell' -e 'end tell' -e 'end tell' -e 'end tell' -e 'end tell' -e 'end tell' -e 'end tell'""")
      return get_first_chrome_url()
    if "Google Chrome 70 got an error: Can’t get window" in x:
      ()if(OSA.log("Can't get window. Have to end all Google Chrome processes and restart again. Click OK to continue. Clicking Abort will abort.",tp=False,buttons=["Abort","OK"])=="OK")else(0/0)
      os.system("killall Google\ Chrome")
      OSA.log("Please restart Google Chrome and navigate to the previous urls",tp=False)
      return get_first_chrome_url(q=q)
    return x
  def openchromeurl(url,wait_time=1):
    x = chromejs("window.location.href = '%s'"%(url))
    if "Google Chrome 70 got an error: Executing JavaScript through AppleScript is turned off." in x:
      if OSA.display_dialog("Google Chrome 70 currently has Executing JavaScript through AppleScript turned off. Turn it on (it will be required for the program to work.)?",text_prompt=False,buttons=["Yes","No"]) == "No":
        return ""
      blueprint('tell application "Google Chrome 70"\n  activate\nend tell\ntell application "System Events"\n  tell process "Google Chrome"\n    tell menu bar 1\n      tell menu bar item "View"\n        tell menu "View"\n          tell menu item "Developer"\n            tell menu "Developer"\n              click menu item "Allow JavaScript from Apple Events"\n            end tell\n          end tell\n        end tell\n      end tell\n    end tell\n  end tell\nend tell')
      os.system("""osascript -e 'tell application "Google Chrome 70"' -e 'activate' -e 'end tell' -e 'tell application "System Events"' -e 'tell process "Google Chrome"' -e 'tell menu bar 1' -e 'tell menu bar item "View"' -e 'tell menu "View"' -e 'tell menu item "Developer"' -e 'tell menu "Developer"' -e 'click menu item "Allow JavaScript from Apple Events"' -e 'end tell' -e 'end tell' -e 'end tell' -e 'end tell' -e 'end tell' -e 'end tell' -e 'end tell'""")
      return openchromeurl(url,wait_time)
    time.sleep(wait_time)
    return x
  def openchromeurls(urls):
    for i in urls:
      openchromeurl(i)
      time.sleep(0.1)
      OSA("Google Chrome 70",["ctrl_t"])
  def safarijs(x):
    blueprint("Safari -> Advanced -> Show develop menu ; Develop -> Allow JavaScript from Apple Events")
    x = 'tell application "Safari" to do JavaScript "%s" in current tab of window 1'%x
    fn = ".%s.scpt" % str(generate_one_random_number(10))
    blueprint(fn)
    open(fn, "w").write(x)
    r = subprocess.getoutput("osascript %s"%fn)
    os.remove(fn)
    return r
    """
    x = "window.location.href = 'https://google.com'"
    safarijs(x)
    """
  globals().update(locals())

