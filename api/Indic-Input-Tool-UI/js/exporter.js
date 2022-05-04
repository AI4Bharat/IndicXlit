// Module to export/save Quill Content

/* LOCAL STORAGE SAVING */

var LAST_SAVE_TIMESTAMP = 0;
var SAVE_CONTENT_FREQUENCY = 5*1000; // millisecs

function saveQuillContentLocally(quill) {
    localStorage.setItem('quill_content', quill.root.innerHTML);
    LAST_SAVE_TIMESTAMP = Date.now();
}

function updateQuillContentLocally(quill) {
    if (Date.now() - LAST_SAVE_TIMESTAMP > SAVE_CONTENT_FREQUENCY) {
        saveQuillContentLocally(quill);
    }
}

function restoreQuillContentFromLocal(quill) {
    // Restore text content if present
    const cached_content = localStorage.getItem('quill_content');
    if (cached_content) {
        quill.root.innerHTML = cached_content;
    }
}

/* EXPORTING QUILL CONTENT AS FILES */

function downloadString(text, fileType, fileName) {
    // https://gist.github.com/danallison/3ec9d5314788b337b682
    var blob = new Blob([text], { type: fileType });
  
    var a = document.createElement('a');
    a.download = fileName;
    a.href = URL.createObjectURL(blob);
    a.dataset.downloadurl = [fileType, a.download, a.href].join(':');
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function() { URL.revokeObjectURL(a.href); }, 1500);
}

function downloadQuillContent(format, quill) {
    if (format == "pdf") {
        var opt = {
            margin:       1,
            filename:     'transcript.pdf',
            html2canvas:  { scale: 2 },
            jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
        html2pdf().set(opt).from(quill.root.innerHTML).save();
    }
    else if (format == "txt") {
        downloadString(quill.getText().trim(), "text/txt", "transcript.txt")
    }
    else if (format == "md") {
        var turndownService = new TurndownService();
        var markdown = turndownService.turndown(quill.root.innerHTML);
        downloadString(markdown, "text/md", "transcript.md")
    }
    else if (format == "html") {
        downloadString(quill.root.innerHTML, "text/html", "transcript.html")
    }
}

function setupQuillExport(quill) {
    const exportDropDown = new QuillToolbarDropDown({
        label: "Export",
        rememberSelection: false
    });
    
    exportDropDown.setItems({
        "PDF": "pdf",
        "Text": "txt",
        "Markdown": "md",
        "HTML": "html"
    });

    exportDropDown.onSelect = function(label, value, quill) {
        downloadQuillContent(value, quill);
        saveQuillContentLocally(quill);
    }

    exportDropDown.attach(quill);
}
