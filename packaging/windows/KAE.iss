#define MyAppName "KAE"
#define MyAppVersion GetEnv("KAE_VERSION")
#if MyAppVersion == ""
#define MyAppVersion "0.1.0"
#endif
#define MyAppPublisher "Kico Audio Lab"
#define MyAppURL "https://github.com/Oleksii1221/KicoAudioEditor"
#define MyAppExeName "KAE.exe"

[Setup]
AppId={{B07D7C89-3D64-45BC-8F19-8E8D3A3D8C52}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={localappdata}\Programs\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
LicenseFile=..\..\LICENSE
OutputDir=..\..\dist\installer
OutputBaseFilename=KAE-Setup-{#MyAppVersion}
SetupIconFile=..\..\src\kae\assets\icons\kae.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "..\..\dist\KAE\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\KAE"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall KAE"; Filename: "{uninstallexe}"
Name: "{autodesktop}\KAE"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch KAE"; Flags: nowait postinstall skipifsilent
