// Get the logo input and color input elements
const logoInput = document.getElementById("logo-input");
const colorPicker = document.getElementById("color-picker");
let qr_link;
let company_name;
let qrcode = undefined;

function set_qr_id(link, name) {
    qr_link = link;
    company_name = name;
    generateQRCode();
}

// Add event listeners to both inputs
try {
    logoInput.addEventListener("change", generateQRCode);
} catch (err) {

}
try {
    colorPicker.addEventListener("change", generateQRCode);
} catch (e) {

}

function generateQRCode() {
    // Get the logo file and color value
    const logo = logoInput.files[0];
    const color = colorPicker.value;
    // Create a new FileReader object to read the logo file
    const reader = new FileReader();

    // Set up the onload function to create the QR code once the file is loaded
    reader.onload = function () {
        if (qrcode === undefined) {
            qrcode = new QRCode(document.getElementById("qrcode"), {// make the QR code with the new logo
                width: 180,
                height: 180,
                text: qr_link,
                logo: reader.result,
                logoWidth: 50,
                logoHeight: 50,
                logoMargin: 10,
                logoBgColor: '#ffffff',
                logoBgTransparent: false,
                colorDark: color,
                colorLight: "#ffffff",
                title: 'Our menu',
                titleFont: "bold 16px Arial",
                titleColor: "#000000",
                titleBackgroundColor: "#ffffff",
                titleHeight: 50,
                titleTop: 15,
                subTitle: company_name,
                subTitleFont: "bold 14px Arial",
                subTitleColor: "#707070",
                subTitleTop: 30,
                correctLevel: QRCode.CorrectLevel.H,
            });
        } else {
            qrcode.clear();
            qrcode = new QRCode(document.getElementById("qrcode"), {
                width: 180,
                height: 180,
                text: qr_link,
                logo: reader.result,
                logoWidth: 50,
                logoHeight: 50,
                logoMargin: 10,
                logoBgColor: '#ffffff',
                logoBgTransparent: false,
                colorDark: color,
                colorLight: "#ffffff",
                title: 'Our menu',
                titleFont: "bold 16px Arial",
                titleColor: "#000000",
                titleBackgroundColor: "#ffffff",
                titleHeight: 50,
                titleTop: 15,
                subTitle: company_name,
                subTitleFont: "bold 14px Arial",
                subTitleColor: "#707070",
                subTitleTop: 30,
                correctLevel: QRCode.CorrectLevel.H,
            });
        }
        // Add a border to the QR code element
        const qrcodeElement = document.getElementById("qrcode");
        const canvasElement = qrcodeElement.querySelector("canvas");
        canvasElement.style.border = "solid 3px #000000";
        canvasElement.style.padding = "0.5rem";
    };

    // Read the logo file as a data URL
    if (logo) {
        reader.readAsDataURL(logo);
    }
}

// Generate normal menu qr
function generateQRCode_2() {
    if (qrcode === undefined) {
        qrcode = new QRCode(document.getElementById("qrcode"), {
            width: 180,
            height: 180,
            text: qr_link,
            colorDark: "#000000",
            colorLight: "#ffffff",
            title: 'Our menu',
            titleFont: "bold 16px Arial",
            titleColor: "#000000",
            titleBackgroundColor: "#ffffff",
            titleHeight: 50,
            titleTop: 15,
            subTitle: company_name,
            subTitleFont: "bold 14px Arial",
            subTitleColor: "#707070",
            subTitleTop: 30,
            correctLevel: QRCode.CorrectLevel.H,
        });
    } else {
        qrcode.clear();
        qrcode = new QRCode(document.getElementById("qrcode"), {
            width: 180,
            height: 180,
            text: qr_link,
            colorDark: "#000000",
            colorLight: "#ffffff",
            title: 'Our menu',
            titleFont: "bold 16px Arial",
            titleColor: "#000000",
            titleBackgroundColor: "#ffffff",
            titleHeight: 50,
            titleTop: 15,
            subTitle: company_name,
            subTitleFont: "bold 14px Arial",
            subTitleColor: "#707070",
            subTitleTop: 30,
            correctLevel: QRCode.CorrectLevel.H,
        });
    }
    // Add a border to the QR code element
    const qrcodeElement = document.getElementById("qrcode");
    const canvasElement = qrcodeElement.querySelector("canvas");
    canvasElement.style.border = "solid 3px #000000";
    canvasElement.style.padding = "0.5rem";
}


// wifi start

// Wifi qr code

const logoInput_1 = document.getElementById("logo-input_1");
const colorPicker_1 = document.getElementById("color-picker_1");
const ssid_div = document.getElementById("wifi_name_qr");
const pw_div = document.getElementById("wifi_password_qr");
let branch_id;
let company_name_1;
let qrcode_1 = undefined;

function set_qr_id_1(id, name) {
    branch_id = id
    company_name_1 = name;
    generateQRCode_1();
}

// Add event listeners to both inputs
try {
    ssid_div.addEventListener("change", generateQRCode_1);
} catch (e) {

}

try {
    pw_div.addEventListener("change", generateQRCode_1);
} catch (e) {

}

try {
    logoInput_1.addEventListener("change", generateQRCode_1);
} catch (e) {

}

try {
    colorPicker_1.addEventListener("change", generateQRCode_1);
} catch (e) {

}

// Generate wifi qr with logo
function generateQRCode_1() {
    // Get the logo file and color value
    const logo_1 = logoInput_1.files[0];
    const color_1 = colorPicker_1.value;
    const ssid = ssid_div.value;
    const pw = pw_div.value;
    const reader_1 = new FileReader();
    reader_1.onload = function () {
        if (qrcode_1 === undefined) {
            qrcode_1 = new QRCode(document.getElementById("qrcode_1"), {// make the QR code with the new logo
                width: 180,
                height: 180,
                text: "WIFI:S:" + ssid + ";T:" + "WPA" + ";P:" + pw + ";H:" + true + ";;",
                logo: reader_1.result,
                logoWidth: 50,
                logoHeight: 50,
                logoBgColor: '#ffffff',
                logoBgTransparent: false,
                colorDark: color_1,
                colorLight: "#ffffff",
                title: "Scan me",
                titleFont: "bold 16px Arial",
                titleColor: "#000000",
                titleBackgroundColor: "#ffffff",
                titleHeight: 50,
                titleTop: 15,
                subTitle: 'Wifi',
                subTitleFont: "bold 14px Arial",
                subTitleColor: "#707070",
                subTitleTop: 30,
                correctLevel: QRCode.CorrectLevel.H,
            });
        } else {
            qrcode_1.clear();
            qrcode_1 = new QRCode(document.getElementById("qrcode_1"), {
                width: 180,
                height: 180,
                text: "WIFI:S:" + ssid + ";T:" + "WPA" + ";P:" + pw + ";H:" + true + ";;",
                logo: reader_1.result,
                logoWidth: 50,
                logoHeight: 50,
                logoBgColor: '#ffffff',
                logoBgTransparent: false,
                colorDark: color_1,
                colorLight: "#ffffff",
                title: "Scan me",
                titleFont: "bold 16px Arial",
                titleColor: "#000000",
                titleBackgroundColor: "#ffffff",
                titleHeight: 50,
                titleTop: 15,
                subTitle: 'Wifi',
                subTitleFont: "bold 14px Arial",
                subTitleColor: "#707070",
                subTitleTop: 30,
                correctLevel: QRCode.CorrectLevel.H,
            });
        }
        const qrcodeElement = document.getElementById("qrcode_1");
        const canvasElement = qrcodeElement.querySelector("canvas");
        canvasElement.style.border = "solid 3px #000000";
        canvasElement.style.padding = "0.5rem";
    };

    // Read the logo file as a data URL
    if (logo_1) {
        reader_1.readAsDataURL(logo_1);
    }
}


// Generate Normal wifi Qr
function generateQRCode_4() {
    const ssid = ssid_div.value;
    const pw = pw_div.value;
    if (qrcode_1 === undefined) {
        qrcode_1 = new QRCode(document.getElementById("qrcode_1"), {
            width: 180,
            height: 180,
            text: "WIFI:S:" + ssid + ";T:" + "WPA" + ";P:" + pw + ";H:" + true + ";;",
            title: "Scan me",
            titleFont: "bold 16px Arial",
            titleColor: "#000000",
            titleBackgroundColor: "#ffffff",
            titleHeight: 50,
            titleTop: 15,
            subTitle: 'Wifi',
            subTitleFont: "bold 14px Arial",
            subTitleColor: "#707070",
            subTitleTop: 30,
            correctLevel: QRCode.CorrectLevel.H,
        });
    } else {
        qrcode_1.clear();
        qrcode_1 = new QRCode(document.getElementById("qrcode_1"), {
            width: 180,
            height: 180,
            text: "WIFI:S:" + ssid + ";T:" + "WPA" + ";P:" + pw + ";H:" + true + ";;",
            title: "Scan me",
            titleFont: "bold 16px Arial",
            titleColor: "#000000",
            titleBackgroundColor: "#ffffff",
            titleHeight: 50,
            titleTop: 15,
            subTitle: 'Wifi',
            subTitleFont: "bold 14px Arial",
            subTitleColor: "#707070",
            subTitleTop: 30,
            correctLevel: QRCode.CorrectLevel.H,
        });
    }
    // Add a border to the QR code element
    const qrcodeElement = document.getElementById("qrcode_1");
    const canvasElement = qrcodeElement.querySelector("canvas");
    canvasElement.style.border = "solid 3px #000000";
    canvasElement.style.padding = "0.5rem";
}
