[Setup]
; Basic App Info
AppName=Word Pro
AppVersion=1.8.1
AppVerName=Word Pro 1.8.1
AppPublisher=Cộng đồng yêu Tiếng Việt
DefaultDirName={autopf}\Word Pro
DefaultGroupName=Word Pro
UninstallDisplayIcon={app}\WordPro.exe

; Force the directory selection page to show
DisableDirPage=no
DisableProgramGroupPage=no

; Compression and Output
Compression=lzma2
SolidCompression=yes
OutputDir=.\Installer
OutputBaseFilename=WordPro_Setup
SetupIconFile=app_icon.ico
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
; Việt hóa các nút bấm và tiêu đề
SetupAppTitle=Trình cài đặt Word Pro
SetupWindowTitle=Trình cài đặt - %1
ButtonNext=Tiếp theo >
ButtonBack=< Quay lại
ButtonInstall=Cài đặt
ButtonOK=Đồng ý
ButtonCancel=Hủy bỏ
ButtonBrowse=Duyệt
ButtonWizardBrowse=Duyệt
ButtonNewFolder=Tạo thư mục mới
ButtonFinish=Hoàn tất
ButtonYes=&Có
ButtonNo=&Không

; Hộp thoại thoát
ExitSetupTitle=Thoát trình cài đặt
ExitSetupMessage=Quá trình cài đặt chưa hoàn tất. Nếu bạn thoát bây giờ, chương trình sẽ không được cài đặt.%n%nBạn có thể chạy lại trình cài đặt vào lúc khác để hoàn tất quá trình cài đặt.%n%nThoát trình cài đặt?

; --- VIỆT HÓA GỠ CÀI ĐẶT (UNINSTALL) ---
ConfirmUninstall=Bạn có chắc chắn muốn gỡ bỏ hoàn toàn %1 và tất cả các thành phần của nó không?
UninstallAppFullTitle=Gỡ bỏ %1
UninstallAppTitle=Gỡ bỏ %1
WizardUninstalling=Đang gỡ bỏ
StatusUninstalling=Đang gỡ bỏ %1...
UninstalledAll=Quá trình gỡ bỏ %1 đã hoàn thành.
UninstalledMost=Quá trình gỡ bỏ %1 đã hoàn tất.%n%nMột số thành phần không thể gỡ bỏ tự động. Bạn có thể xóa chúng thủ công.

; Trang chào mừng
WelcomeLabel1=Chào mừng bạn đến với trình cài đặt Word Pro
WelcomeLabel2=Trình khởi tạo này sẽ cài đặt phiên bản %2 vào máy tính của bạn.%n%nVui lòng đóng tất cả các ứng dụng khác trước khi tiếp tục.
WizardSelectDir=Chọn vị trí cài đặt
SelectDirDesc=Bạn muốn cài đặt Word Pro vào đâu?
SelectDirLabel3=Trình cài đặt sẽ cài đặt Word Pro vào thư mục sau.
SelectDirBrowseLabel=Để tiếp tục, hãy nhấn Tiếp theo. Nếu bạn muốn chọn một thư mục khác, hãy nhấn Duyệt.

WizardSelectProgramGroup=Chọn thư mục Start Menu
SelectStartMenuFolderDesc=Trình cài đặt sẽ tạo các biểu tượng tắt trong thư mục Start Menu sau.
SelectStartMenuFolderLabel3=Trình cài đặt sẽ tạo các biểu tượng tắt trong thư mục Start Menu sau.
SelectStartMenuFolderBrowseLabel=Để tiếp tục, nhấn Tiếp theo. Để chọn thư mục khác, nhấn Duyệt.

WizardSelectTasks=Chọn tác vụ bổ sung
SelectTasksLabel2=Những tác vụ bổ sung nào cần được thực hiện?
SelectTasksDesc=Chọn các tác vụ bổ sung mà bạn muốn thực hiện, sau đó nhấn Tiếp theo.

WizardReady=Sẵn sàng cài đặt
ReadyLabel1=Trình cài đặt đã sẵn sàng để bắt đầu cài đặt vào máy tính của bạn.
ReadyLabel2a=Nhấn Cài đặt để bắt đầu quá trình cài đặt.
ReadyLabel2b=Nhấn Cài đặt để bắt đầu quá trình cài đặt.
ReadyMemoDir=Vị trí cài đặt:
ReadyMemoGroup=Thư mục Start Menu:
ReadyMemoTasks=Tác vụ bổ sung:

WizardInstalling=Đang cài đặt
InstallingLabel=Vui lòng đợi trong khi trình cài đặt cài đặt Word Pro trên máy tính của bạn.
StatusExtractFiles=Đang giải nén tập tin...

FinishedHeadingLabel=Hoàn tất cài đặt Word Pro
FinishedLabelNoIcons=Quá trình cài đặt Word Pro đã hoàn thành.
FinishedLabel=Quá trình cài đặt đã hoàn thành. Bạn có thể khởi chạy ứng dụng ngay bây giờ.
ClickFinish=Nhấn Hoàn tất để thoát khỏi trình cài đặt.

[Code]
// Dùng code để ép kiểu dòng dung lượng ổ đĩa (Fix lỗi %1)
procedure InitializeWizard;
begin
  WizardForm.DiskSpaceLabel.Caption := 'Yêu cầu ít nhất 72 MB dung lượng đĩa trống.';
end;

[Files]
Source: "dist\WordPro\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Word Pro"; Filename: "{app}\WordPro.exe"
Name: "{autodesktop}\Word Pro"; Filename: "{app}\WordPro.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Tạo biểu tượng ngoài màn hình Desktop (Shortcut)"; GroupDescription: "Tùy chọn thêm:"

[Run]
Filename: "{app}\WordPro.exe"; Description: "Khởi chạy Word Pro ngay bây giờ"; Flags: nowait postinstall
