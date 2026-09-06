<#
.SYNOPSIS
    Genera la estructura de directorios excluyendo carpetas especificas.
.DESCRIPTION
    Crea un archivo de texto con la estructura del proyecto, omitiendo .venv y otras carpetas.
    Incluye estadisticas del proyecto y opciones de personalizacion.
.PARAMETER OutputDir
    Directorio donde se guardara el archivo de salida. Por defecto es el directorio actual.
.PARAMETER ExcludeFolders
    Array de nombres de carpetas a excluir del arbol.
.PARAMETER MaxDepth
    Profundidad maxima del arbol a mostrar (por defecto 3). Usa 0 para profundidad ilimitada.
.PARAMETER ExcludeHidden
    Switch para excluir carpetas y archivos ocultos.
.EXAMPLE
    .\Get-Structure.ps1
.EXAMPLE
    .\Get-Structure.ps1 -ExcludeFolders @('.venv', 'node_modules', '.git') -MaxDepth 2
.EXAMPLE
    .\Get-Structure.ps1 -ExcludeFolders @('.venv') -ExcludeHidden -OutputDir "C:\Reports"
.NOTES
    Autor: PowerShell Expert
    Fecha: 2026
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$OutputDir = ".",

    [Parameter(Mandatory = $false)]
    [string[]]$ExcludeFolders = @('.venv', 'node_modules', '__pycache__', '.git', '.idea', '.vscode', 'dist', 'build'),

    [Parameter(Mandatory = $false)]
    [int]$MaxDepth = 3,

    [Parameter(Mandatory = $false)]
    [switch]$ExcludeHidden,

    [Parameter(Mandatory = $false)]
    [string]$OutputFileName = "estructura_$(Get-Date -Format yyyyMMdd_HHmm).txt"
)

# Configurar encoding
$global:OutputEncoding = [System.Text.Encoding]::UTF8

# Validar directorio de salida
if (!(Test-Path $OutputDir)) {
    Write-Warning "El directorio '$OutputDir' no existe. Se creara automaticamente."
    New-Item -Path $OutputDir -ItemType Directory -Force | Out-Null
}

$outputPath = Join-Path $OutputDir $OutputFileName

# Funcion para generar estructura personalizada
function Get-CustomTree {
    param(
        [string]$Path = ".",
        [string]$Indent = "",
        [int]$Depth = 0
    )

    $items = Get-ChildItem $Path | Where-Object {
        $exclude = $false

        # Verificar si es una carpeta o archivo oculto
        if ($ExcludeHidden -and $_.Attributes -match 'Hidden') {
            $exclude = $true
        }

        # Verificar si esta en la lista de exclusion
        if ($_.Name -in $ExcludeFolders) {
            $exclude = $true
        }

        # Verificar si es una carpeta y empezar con punto (Unix hidden)
        if ($_.PSIsContainer -and $_.Name.StartsWith('.')) {
            $exclude = $true
        }

        return -not $exclude
    }

    # Ordenar: primero carpetas, luego archivos
    $sortedItems = $items | Sort-Object {
        if ($_.PSIsContainer) { 0 } else { 1 }
    }, Name

    $itemCount = $sortedItems.Count

    for ($i = 0; $i -lt $itemCount; $i++) {
        $item = $sortedItems[$i]
        $isLast = ($i -eq $itemCount - 1)

        # Determinar simbolos segun el nivel
        if ($Depth -eq 0) {
            $symbol = "+-- "
            if ($isLast) { $symbol = "\-- " }
        } else {
            $symbol = if ($isLast) { "\-- " } else { "+-- " }
        }

        # Mostrar carpeta o archivo con indicador
        $type = if ($item.PSIsContainer) { "[DIR]" } else { "[FILE]" }
        $outputLine = "$Indent$symbol$($item.Name) $type"

        Write-Output $outputLine

        # Recursion para carpetas
        if ($item.PSIsContainer) {
            if ($MaxDepth -eq 0 -or $Depth -lt $MaxDepth) {
                $newIndent = if ($isLast) { "$Indent    " } else { "$Indent|   " }
                Get-CustomTree -Path $item.FullName -Indent $newIndent -Depth ($Depth + 1)
            }
        }
    }
}

# Funcion para obtener estadisticas
function Get-Statistics {
    param([string]$Path = ".")

    Write-Output "`n" + ("=" * 60)
    Write-Output "ESTADISTICAS DEL PROYECTO"
    Write-Output ("=" * 60)

    # Obtener todos los items excluyendo carpetas especificadas
    $allItems = Get-ChildItem -Path $Path -Recurse -Force | Where-Object {
        $exclude = $false
        $relativePath = $_.FullName.Substring((Get-Location).Path.Length + 1)
        $pathParts = $relativePath -split '\\'

        foreach ($folder in $ExcludeFolders) {
            if ($pathParts -contains $folder) {
                $exclude = $true
                break
            }
        }
        if ($ExcludeHidden -and $_.Attributes -match 'Hidden') { $exclude = $true }
        return -not $exclude
    }

    $totalFiles = ($allItems | Where-Object { -not $_.PSIsContainer }).Count
    $totalDirs = ($allItems | Where-Object { $_.PSIsContainer }).Count
    $totalSize = ($allItems | Where-Object { -not $_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum

    # Calcular tamaño en formato legible
    $sizeString = ""
    if ($totalSize -gt 1GB) {
        $sizeString = "{0:N2} GB" -f ($totalSize / 1GB)
    } elseif ($totalSize -gt 1MB) {
        $sizeString = "{0:N2} MB" -f ($totalSize / 1MB)
    } elseif ($totalSize -gt 1KB) {
        $sizeString = "{0:N2} KB" -f ($totalSize / 1KB)
    } else {
        $sizeString = "$totalSize bytes"
    }

    Write-Output "Total directorios: $totalDirs"
    Write-Output "Total archivos: $totalFiles"
    Write-Output "Tamaño total: $sizeString"

    # Obtener top 5 tipos de archivo mas comunes
    $fileExtensions = $allItems | Where-Object { -not $_.PSIsContainer } |
        ForEach-Object { [System.IO.Path]::GetExtension($_.Name) } |
        Where-Object { $_ -ne '' } |
        Group-Object |
        Sort-Object Count -Descending |
        Select-Object -First 5

    Write-Output "`nTop 5 extensiones de archivo:"
    if ($fileExtensions) {
        foreach ($ext in $fileExtensions) {
            Write-Output "   - $($ext.Name): $($ext.Count) archivos"
        }
    } else {
        Write-Output "   No se encontraron archivos con extensiones."
    }

    # Mostrar las carpetas excluidas
    Write-Output "`nCarpetas excluidas:"
    foreach ($folder in $ExcludeFolders) {
        Write-Output "   - $folder"
    }

    Write-Output ("=" * 60)
}

# Funcion principal
function Main {
    Write-Host "Generando estructura de directorios..." -ForegroundColor Cyan
    Write-Host "Directorio base: $(Get-Location)" -ForegroundColor Gray
    Write-Host "Profundidad maxima: $(if ($MaxDepth -eq 0) { 'Ilimitada' } else { $MaxDepth })" -ForegroundColor Gray
    Write-Host "Carpetas excluidas: $($ExcludeFolders -join ', ')" -ForegroundColor Gray
    Write-Host "`n" -ForegroundColor Gray

    # Construir el contenido
    $content = @()
    $content += "=" * 80
    $content += "ESTRUCTURA DE DIRECTORIOS"
    $content += "=" * 80
    $content += "Proyecto: $(Split-Path (Get-Location) -Leaf)"
    $content += "Ruta: $(Get-Location)"
    $content += "Fecha: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')"
    $content += "=" * 80
    $content += "`n"

    # Generar el arbol
    $treeLines = Get-CustomTree
    $content += $treeLines

    # Agregar estadisticas
    $statistics = Get-Statistics | Out-String
    $content += $statistics

    # Guardar archivo
    try {
        $content | Out-File -FilePath $outputPath -Encoding UTF8 -Force
        Write-Host "Estructura guardada en: $outputPath" -ForegroundColor Green

        # Mostrar informacion del archivo
        $fileInfo = Get-Item $outputPath
        $fileSize = if ($fileInfo.Length -gt 1KB) {
            "{0:N2} KB" -f ($fileInfo.Length / 1KB)
        } else {
            "$($fileInfo.Length) bytes"
        }
        Write-Host "Tamaño del archivo: $fileSize" -ForegroundColor Yellow

        # Preguntar si se quiere abrir el archivo
        $openFile = Read-Host "`nDesea abrir el archivo? (S/N)"
        if ($openFile -eq 'S' -or $openFile -eq 's') {
            Start-Process $outputPath
        }

    } catch {
        Write-Error "Error al guardar el archivo: $_"
        return 1
    }
    
    return 0
}

# Ejecutar script
$exitCode = Main
exit $exitCode