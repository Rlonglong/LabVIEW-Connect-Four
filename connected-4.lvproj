<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="25008000">
	<Property Name="NI.LV.All.SaveVersion" Type="Str">25.0</Property>
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="AIMove.vi" Type="VI" URL="../sub vi/AIMove.vi"/>
		<Item Name="AIMove_MinMax.vi" Type="VI" URL="../sub vi/AIMove_MinMax.vi"/>
		<Item Name="bc1.ctl" Type="VI" URL="../sub vi/bc1.ctl"/>
		<Item Name="bc2.ctl" Type="VI" URL="../sub vi/bc2.ctl"/>
		<Item Name="bc3.ctl" Type="VI" URL="../sub vi/bc3.ctl"/>
		<Item Name="CheckMove.vi" Type="VI" URL="../sub vi/CheckMove.vi"/>
		<Item Name="CheckWin.vi" Type="VI" URL="../sub vi/CheckWin.vi"/>
		<Item Name="Drawboard.vi" Type="VI" URL="../sub vi/Drawboard.vi"/>
		<Item Name="DrawHover.vi" Type="VI" URL="../sub vi/DrawHover.vi"/>
		<Item Name="GetValidMoves.vi" Type="VI" URL="../sub vi/GetValidMoves.vi"/>
		<Item Name="Global Variable.vi" Type="VI" URL="../Global Variable.vi"/>
		<Item Name="IsBoardFull.vi" Type="VI" URL="../sub vi/IsBoardFull.vi"/>
		<Item Name="main.vi" Type="VI" URL="../main.vi"/>
		<Item Name="PlacePiece.vi" Type="VI" URL="../sub vi/PlacePiece.vi"/>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
