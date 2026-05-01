Get-NetTCPConnection | Where-Object { $_.State -eq 'Listen' -and ($_.LocalPort -eq 1433 -or $_.LocalPort -eq 1434 -or $_.OwningProcess -eq 3572) } | Select-Object LocalAddress,LocalPort,State,OwningProcess | Format-Table -AutoSize

Write-Host '---'
Get-Service -Name SQLBrowser | Select-Object Name,Status,DisplayName | Format-Table -AutoSize

Write-Host '---'
Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQLServer\SuperSocketNetLib\Tcp\IPAll' | Select-Object TcpPort,TcpDynamicPorts | Format-List
Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQLServer\SuperSocketNetLib\Np' | Select-Object Enabled,PipeName | Format-List
