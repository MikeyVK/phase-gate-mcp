$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    node ./probe.mjs
    $probeBase = ([Uri]($PSScriptRoot.Replace('\', '/') + '/')).AbsoluteUri
    $logicalUrl = $probeBase + 'workspace/docs/guides/installatie.md'
    foreach ($fixture in @('scratch', 'scratch-valid')) {
        $physicalUrl = $probeBase + $fixture + '/installatie.md'
        $remap = '^' + [regex]::Escape($logicalUrl) + '(#.*)?$ ' + $physicalUrl + '$1'
        & ./bin/lychee-x86_64-pc-windows-msvc/lychee.exe --offline --cache=false --include-fragments --format json --base-url $logicalUrl --remap $remap "$fixture/installatie.md"
        Write-Output "Fixture=$fixture ExitCode=$LASTEXITCODE"
    }
    Write-Output "Intended target exists: $(Test-Path -LiteralPath ./workspace/docs/guides/installatie.md)"
} finally {
    Pop-Location
}
