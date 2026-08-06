# fix_styling.ps1 — Batch apply styling to all OPS4 course pages
# Run from the OPS4_html root directory

$root = $PSScriptRoot
if (-not $root) { $root = Get-Location }

# ============================================================
# 1. GLOSSARY TOOLTIP CSS — Add to all pages missing it
# ============================================================
$glossaryCSS = @"
        /* Glossary Tooltip */
        .glossary-term { color: #c9984a; border-bottom: 2px dotted #c9984a; cursor: help; position: relative; text-decoration: none; }
        .glossary-term:hover { color: #002F6E; }
        html.dark .glossary-term:hover { color: #ffffff; }

"@

$allHtml = Get-ChildItem -Path $root -Recurse -Filter "*.html" | Where-Object { $_.Name -ne "index.html" }

foreach ($file in $allHtml) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    $changed = $false

    # Add glossary CSS if missing
    if ($content -notmatch 'glossary-term') {
        $content = $content -replace '(        /\* OPS3-Style Code Blocks)', "$glossaryCSS`$1"
        $changed = $true
    }

    # Remove the duplicate back-link and raw H1 (pattern: <p><a href="../OPS4_COURSE_STRUCTURE.md">... followed by <h1>...)
    if ($content -match '<p><a href="\.\./OPS4_COURSE_STRUCTURE\.md">') {
        # Remove the back link paragraph
        $content = $content -replace '            <p><a href="\.\./OPS4_COURSE_STRUCTURE\.md">.*?</a></p>\r?\n', ''
        $changed = $true
    }

    # Remove duplicate raw H1 that repeats the banner title (lines like <h1>Week X: Topic - Student Notes</h1>)
    # followed by the raw Course/Module/Week paragraph
    $h1Pattern = '<h1>Week \d+:.*?</h1>\r?\n<p><strong>Course</strong>.*?<strong>Week</strong>.*?\d+</p>\r?\n'
    if ($content -match $h1Pattern) {
        $content = $content -replace $h1Pattern, ''
        $changed = $true
    }
    # Also handle standalone duplicate H1 (without the metadata paragraph following)
    # Only remove if there's already a banner h1 above it
    $standaloneH1 = '<h1>Week \d+ Lab:.*?</h1>\r?\n<p><strong>Objective</strong>'
    if ($content -match $standaloneH1) {
        $content = $content -replace '<h1>Week \d+ Lab:.*?</h1>\r?\n', ''
        $changed = $true
    }

    if ($changed) {
        Set-Content $file.FullName -Value $content -Encoding UTF8 -NoNewline
        Write-Host "Updated: $($file.Name)" -ForegroundColor Green
    } else {
        Write-Host "Skipped (no changes): $($file.Name)" -ForegroundColor DarkGray
    }
}

# ============================================================
# 2. ADD PREV/NEXT NAVIGATION to Student Notes pages
# ============================================================

$weekFolders = @(
    @{ Num=1;  Folder="Week 1 - HPC Introduction and Architectures"; Title="HPC Introduction" },
    @{ Num=2;  Folder="Week 2 - System Design and Memory"; Title="System Design" },
    @{ Num=3;  Folder="Week 3 - Node Provisioning"; Title="Node Provisioning" },
    @{ Num=4;  Folder="Week 4 - Resource Management"; Title="Resource Management" },
    @{ Num=5;  Folder="Week 5 - Benchmarking and Tuning"; Title="Benchmarking" },
    @{ Num=6;  Folder="Week 6 - Parallel Programming"; Title="Parallel Programming" },
    @{ Num=7;  Folder="Week 7 - Parallel Algorithms"; Title="Parallel Algorithms" },
    @{ Num=8;  Folder="Week 8 - Advanced Storage Concepts"; Title="Advanced Storage" },
    @{ Num=9;  Folder="Week 9 - Accelerators"; Title="Accelerators" },
    @{ Num=10; Folder="Week 10 - HPC Applications"; Title="HPC Applications" },
    @{ Num=11; Folder="Week 11 - Cluster Monitoring"; Title="Cluster Monitoring" },
    @{ Num=12; Folder="Week 12 - Capstone Project"; Title="Capstone Project" }
)

foreach ($i in 0..($weekFolders.Count - 1)) {
    $week = $weekFolders[$i]
    $notesFile = Join-Path $root "$($week.Folder)\Week_$($week.Num)_Student_Notes.html"
    
    if (-not (Test-Path $notesFile)) { continue }

    $content = Get-Content $notesFile -Raw -Encoding UTF8

    # Build prev link
    $prevNav = ""
    if ($i -gt 0) {
        $prev = $weekFolders[$i - 1]
        $prevUrl = "../$([uri]::EscapeDataString($prev.Folder))/Week_$($prev.Num)_Student_Notes.html"
        $prevNav = @"

                        <a href="$prevUrl" class="group flex flex-col items-center hover:text-primary dark:hover:text-sky-400 transition-colors">
                            <div class="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 mb-1">
                                <svg class="w-6 h-6 text-slate-400 group-hover:text-primary dark:group-hover:text-sky-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
                            </div>
                            <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider group-hover:text-primary dark:group-hover:text-sky-400">Week $($prev.Num)</span>
                        </a>
                        
"@
    }

    # Build next link
    $nextNav = ""
    if ($i -lt ($weekFolders.Count - 1)) {
        $next = $weekFolders[$i + 1]
        $nextUrl = "../$([uri]::EscapeDataString($next.Folder))/Week_$($next.Num)_Student_Notes.html"
        $nextNav = @"

                        <a href="$nextUrl" class="group flex flex-col items-center hover:text-primary dark:hover:text-sky-400 transition-colors">
                            <div class="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 mb-1">
                                <svg class="w-6 h-6 text-slate-400 group-hover:text-primary dark:group-hover:text-sky-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                            </div>
                            <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider group-hover:text-primary dark:group-hover:text-sky-400">Week $($next.Num)</span>
                        </a>
                        
"@
    }

    # Replace the bottom dock — find the existing dock and replace it with nav-enhanced version
    $dockPattern = '<div class="fixed bottom-4 left-1/2.*?</div>\r?\n\r?\n</body>'
    
    $newDock = @"
<div class="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-white/90 dark:bg-slate-900/90 backdrop-blur border border-gray-200 dark:border-gray-700 rounded-full shadow-2xl px-6 py-2 flex items-center space-x-8 z-50">
    $prevNav
    <a href="../index.html" class="group relative flex items-center justify-center p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
        <div class="w-10 h-10 rounded-full bg-primary flex items-center justify-center shadow-lg border-2 border-secondary group-hover:scale-110 transition-transform">
             <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
        </div>
        <span class="absolute -top-10 left-1/2 transform -translate-x-1/2 bg-slate-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">Course Index</span>
    </a>
    $nextNav
</div>

</body>
"@

    if ($content -match '(?s)<div class="fixed bottom-4 left-1/2.*?</div>\s*</body>') {
        $content = $content -replace '(?s)<div class="fixed bottom-4 left-1/2.*?</div>\s*</body>', $newDock
        Set-Content $notesFile -Value $content -Encoding UTF8 -NoNewline
        Write-Host "Nav updated: Week $($week.Num) Student Notes" -ForegroundColor Cyan
    }
}

Write-Host "`nDone! All pages updated." -ForegroundColor Yellow
