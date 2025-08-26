#define AppName "YouTube Downloader"
#define AppExeName "youtube-downloader.exe"
#define AppVersion "0.1"
#define AppPublisher "Vasco Vicente"
#define AppPublisherURL "https://github.com/sudoppo"
#define AppSupportURL "https://github.com/sudoppo/youtube-downloader"

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppPublisherURL}
AppSupportURL={#AppSupportURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
UninstallDisplayIcon={app}\{#AppExeName}
Compression=lzma2/ultra64
SolidCompression=yes
OutputDir=.\dist
OutputBaseFilename=YouTubeDownloaderSetup_{#AppVersion}
SetupIconFile=assets\icons\youtube-icon.ico
WizardStyle=modern
WizardSmallImageFile=assets\wizard-image.bmp
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=no
PrivilegesRequired=lowest
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Files]
; Main executable
Source: ".\dist\YouTube Downloader.exe"; DestDir: "{app}"; DestName: "{#AppExeName}"; Flags: ignoreversion

; FFmpeg binaries
Source: ".\bin\ffmpeg.exe"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: ".\bin\ffprobe.exe"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: ".\bin\ffplay.exe"; DestDir: "{app}\bin"; Flags: ignoreversion

; Include the icon file
Source: "assets\youtube-icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\youtube-icon.ico"
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; IconFilename: "{app}\youtube-icon.ico"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent;

[InstallDelete]
; Clean up old versions
Type: files; Name: "{app}\bin\*.*"
Type: filesandordirs; Name: "{app}\lib\*.*"

[UninstallDelete]
Type: filesandordirs; Name: "{app}\temp"
Type: files; Name: "{app}\*.log"

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Optional: Add installation directory to PATH
    // RegWriteStringValue(HKEY_CURRENT_USER, 'Environment', 'YouTubeDownloader', ExpandConstant('{app}'));
  end;
end;



