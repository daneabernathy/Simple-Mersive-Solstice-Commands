## OpenControl API 1.0 Guide

- [OpenControl API for Solstice](#opencontrol-api-for-solstice)
- [Using the OpenControl API](#using-the-opencontrol-api)
  - [JSON Record Structure](#json-record-structure)
  - [Securing API Communications](#securing-api-communications)
  - [Basic GET](#basic-get)
  - [Basic POST](#basic-post)
  - [GET/POST Example Script (Python 2.7)](#getpost-example-script-python-27)
- [Tips for Writing Your Own Script](#tips-for-writing-your-own-script)
- [Configuration API](#configuration-api)
  - [Product/Global Settings](#productglobal-settings)
  - [Solstice Display Communications Settings](#solstice-display-communications-settings)
  - [Global Display Settings](#global-display-settings)
  - [Authentication Modes](#authentication-modes)
  - [Main Network and Feature Record](#main-network-and-feature-record)
  - [RSS Feeds](#rss-feeds)
  - [Forget Wireless Network](#forget-wireless-network)
  - [Licensing](#licensing)
  - [Passwords](#passwords)
  - [System Settings Record](#system-settings-record)
  - [Splashscreen Commands](#splashscreen-commands)
  - [Power Management](#power-management)
  - [Power Management Commands](#power-management-commands)
  - [HDMI Input](#hdmi-input)
  - [Calendar API](#calendar-api)
  - [Calendar Settings](#calendar-settings)
  - [Calendar Commands](#calendar-commands)
  - [Other APIs](#other-apis)
    - [Version and Update Control API](#version-and-update-control-api)
    - [Passing RS-232 Controls API](#passing-rs-232-controls-api)
    - [Other API-Related Tasks](#other-api-related-tasks)
    - [Stats API](#stats-api)
    - [Global Stats Record](#global-stats-record)
  - [Command API](#command-api)
  - [Solstice Discovery Services (SDS) API](#solstice-discovery-services-sds-api)
  - [SDS Commands](#sds-commands)
  - [Valid Time Zone Values](#valid-time-zone-values)

# OpenControl API for Solstice

The OpenControl protocol supports third-party integration with Solstice Pods through a simple RESTful API. OpenControl can be an important component in a Solstice deployment because it allows integrators and installers to more deeply integrate Solstice with existing room infrastructure.

For example, it can be used to monitor the status of a Solstice Pod, capture usage statistics, and configure endpoints.

OpenControl exposes much of the functionality found in the Solstice Dashboard through a straightforward communications protocol that can be read/written both by humans and machines.

Creative uses of the API include automatically emailing IT administrators when a Pod’s new settings do not meet enterprise security standards and enabling dynamic switching between input sources for digital signage.

OpenControl uses HTTP GET and POST commands to receive and send data to a Solstice Pod. The approach ensures that the API is composed of simple transactions that can be sent to a Pod without requiring complex management of state by a 3rd party developer. Any language, on any device, that can issue HTTP GET and POST commands to the appropriate URLs of the Solstice Pod, then, can be integrated into a Solstice deployment.

What is Required to use the OpenControl API?
1. Solstice Pod or Solstice Windows Software host with an Enterprise Edition license.
        Note that the Pod and Windows host respond differently to different commands and that some commands are Pod or Windows only; see command list for details.
2. A client platform for issuing commands to the Solstice Pod.
3. A network connection between the client and Solstice Pod.

Example Uses of the OpenControl API

- Capturing statistical usage data periodically and storing that data ina third-party database for analytics.
- Integrating configuration options into a third-party IT dashboard suite, allowing IT dashboards to incorporate status information about a Solstice deployment.
- Clearing the screen of posted content or booting users from a Solstice session from in-room control panels.
- Displaying information about a Solstice session - for example the Session Key - on acontrol panel or second display.
- Updating the Solstice Pod splash-screen messaging from a third-party application.

The OpenControl communications protocol uses JSON structures to exchange information between the Solstice Pod and any number of clients. The protocol uses port 80 or 443 Solstice Pods receive request records and respond to requests by either carrying out an action (i.e. modifying configuration, performing an action) or by responding with a JSON response.

OpenControl clients can only communicate with Enterprise Edition Solstice Pods. Standard Solstice Pods (i.e. non-Enterprise Edition) need to be upgraded to Enterprise Edition before using the OpenControl API. The figure below depicts the main components needed to implement OpenControl.

Solstice Enterprise Host <--Network Interconnect Port 80/443--> OpenControl Client Platform OpenControl Client Platform --GET/POST JSON Records to IPAddress/--> Solstice Enterprise Host --JSON Response--> OpenControl Client Platform

OpenControl operates over existing TCP/IP network infrastructure to allow third-party client platforms to control and query Solstice endpoints. The protocol is based on a REST architecture that encapsulates communication into independent GET/POST events, sent to particular URLs on the Solstice Pods, each of which result in a JSON formatted response.

# Using the OpenControl API

The OpenControl API protocol is divided into areas based on functional types. These types are: Config, Stats, and Command. Eachis associated with a different URL. By sending an appropriately formatted JSON record to the corresponding URL, third-party developers can query and set values or settings related to the Solstice Pod. These URLs are:
```
/api/config
```
  - Used for posting and getting information related to administrative configuration of Solstice Pod. For example, modifying the network settings of a Pod.
```
/api/stats
```
- Used to get instantaneous status about a Solstice Pod. For example, capturing the number of users currently connected to a Solstice Windows Software endpoint
> Mersive does not currently recommend polling Solstice Pods via API more than once
every 10 seconds.
```
/api/control
```
- Used to post commands to a Solstice Pod that impacts runtime behavior. For example, clearing a screen of all media.
- Other URLs are used in the Calendar and Version APIs. See the Calendar API and Version and Update Control API! topics for more details.

Users of OpenControl can set values by using a POST structure to the appropriate URL. This is used to modify configuration, or POST actions to a Solstice Pod to control runtime behavior. In addition, users can query current configuration and status using GET commands to the appropriate URL.

## JSON Record Structure

POST and GET records sent to and received from the different URLs are made up of key/value pairs that represent the various capabilities exposed through the API. This structure uses the JSON syntax. Example:
```
{ key1: value1, key2: value2, .. keyN, valueN }
```
POST records do not need to contain all key/value pairs and can contain any subset of key/values based on the needs of the integration. The order of a request record is not important, so long as the key/value pairs follow the format above. For example, POSTing the string ‘{key2:value2} to the appropriate URL of a Solstice Pod can set that value.
In some cases, key/value pairs are organized hierarchically based on logical groupings. In these cases, the JSON syntax is simply nested within the value of a particular key. Those key/value pairs appear within brackets and are separated from other key/value pairs with a comma. Example:
```
 { key1:v alue1, key2: value2, GroupKey:{ NestedKey1: GroupValue1, .., NestedKeyN: GroupValueN }, key3: value3 }
```
This represents a JSON structure that contains three key/value pairs at the top level, and a set of key/value pairs that are grouped within ‘GroupKey’.
Using this syntax, for example, a user could set the display name for a particular Solstice Pod by sending the following JSON record:
```
{ m_displayInformation: { m_displayName: ‘NewDisplayName’ } }
```

## Securing API Communications

To ensure that only valid third-party users are able to communicate with Solstice Pods, the administration password, when set, must be provided with each POST or GET record. The administration password, for a particular Pod, can be set both in the Solstice Pod Configuration Panel, or through the Solstice Dashboard.
> If no password is set, then any third-party application can use the OpenControl APIs to modify a Solstice Pod over the network.

When an administrator password is set, each POST request record must include a key/value pair that is: ‘password: admin_password’ at the top level of the record. A request record sent to a Solstice Pod that has password enabled, then, must follow this format:
> { password: admin_password, key1: value1, key2: value2, .. keyN, valueN }

In the case of a GET record, the password is simply appended to the GET URL request as follows:
> ?password=admin_password

## Basic GET

There are two URLs for each IP address that respond with text to a GET command. For our example IP address of 192.168.3.127, the valid URLs are:
> http://192.168.3.127/api/stats
>
> http://192.168.3.127/api/config

While there is some overlap in information, the “stats” URL generally gives a snapshot of important values and instantaneous usage while the “config” URL gives more detail about everything from enabled options to appear screen layout. Note that while you can GET from either URL, you can only POST to /api/config.

To test the stats URL, set up your environment as described in the previous section and send the following command (with your own URL):
> rs=requests.get (*http://192.168.3.127/api/stats’ )

If you have an admin password protecting access to the display, append the password in the following way, with “adminpassword” as whatever the actual password is for the display.
> rs=requests.get (*http://192.168.3.127/api/stats?password=adminpassword’ )

To display the raw results, type:
> rs.text

You should see a continuous chunk of text with the first distinct value of “m_displayID”. To pull out a specific value in a clean format, the string needs to be converted to a dictionary of key:value pairs.
> rstats = eval(rs.text)

If you print the new value (rstats.text) you still see a chunk of continuous text, but the formatting is slightly different. We can now use get() to find specific terms, like the display name. m_displayName is a part of the m_displayInformation group key, so we use nested get() commands:
> print “Display Name:”, rstats.get (*‘m_displayInformation’, {}).get (‘m_displayName’ )

The result should be “Display Name: Pikes Peak” with the actual display name reflecting the name on your Solstice display. Any of the values can be pulled from the list in this manner.

## Basic POST

Many of the key:value pairs that can be read using GET can also be changed through the API using POST. While the same values may appear in the GET of both URLs, POSTs may only be sent to the /api/config URL:
> http://192.168.3.127/api/config

The requests command now changes from GET to POST and requires a payload parameter. To change the display name, use the following command:
```
r=requests.post (‘http://192.168.3.207/api/config’, json={ ‘m_displayInformation’ :{ ‘m_displayName’ :’New Name’ }})
```
If you have an admin password protecting the display, send the following command where ‘adminpassword’ is the actual password for the display:
```
r=requests.post (‘http://192.168.3.207/api/config’, json={ ‘password’: ‘admin_password’, ‘m_displayInformation’:{‘m_displayName’ :’New Name’ }})
```
If you copy either of these lines directly into Python or a formatted text editor and get a syntax error, the single quotes are likely to blame. They may come through formatted such that requests.post(} does not recognize them. If this happens, manually delete each mark and re-enter it in the terminal window to get the appropriate format.

To see the new name, run GET on the same URL and look for the ‘m_displayName’ key, which should now have a value of ‘New Name:
```
re=requests.get (‘http://192.168.3.127/api/config’ )
reonfig=eval (rc.text)
print “Display Name:”, rconfig.get (‘m_displayInformation’, {}).get (‘m_displayName’ )
```

If you have an admin password protecting the display, you need to add in the password as before.

## GET/POST Example Script (Python 2.7)

The complete script provides additional comments and the option for an admin password. Download the complete script here (https://github.com/LauraMersive/APldemo/blob/master/OpenControlGETPOSTdemo.py).

This pared down version gets the Display Name from both /config and /stats URLs, changes the name, then gets both values again to confirm the name has changed.

```
import sys
import sys
import requests
import random
from random import choice

true=1
false=0

newname = “New Name”
myurl = “http://192.168.3.227”
admin_password = “”

mystatsurl = myurl+’/api/stats’
myconfigurl = myurl+’/api/config’

rs=requests.get(mystatsurl)
rc=requests.get(myconfigurl)
rstats=eval(rs.text)
rconfig=eval(rc.text)

print “Current Display Name from Stats:”,
rstats.get(‘m_displayInformation’,{}).get(‘m_displayName’)

print “Current Display Name from Config:”,
rconfig.get(‘m_displayInformation’,{}).get(‘m_displayName’)

r=requests.post(myconfigurl, json= {‘password’:’admin_password’,’m_displayInformation’: {‘m_displayName’:newname}})
print “Changing Name to: “,newname
print “.............”

rs=requests.get(mystatsurl)
rc=requests.get(myconfigurl)
rstats=eval(rs.text)
rconfig=eval(rc.text)
print “New Display Name from Stats:”,rstats.get(‘m_displayInformation’,{}).get(‘m_displayName’)
print “New Display Name from Config:”,rconfig.get(‘m_displayInformation’,{}).get(‘m_displayName’)

```
# Tips for Writing Your Own Script

If you start writing your own script, you need to import the requests package before attempting to
execute any GET/POST code. You also need to import sys, and likely want time as well. Though it seems
redundant, you can avoid errors later on by explicitly defining true=1 and false=0 in your new Python
window or at the top of your script.

In general, start with all the following commands:
```
import sys
import time
import datetime
import requests
import json
true=1
false=0
```

# Configuration API

Solstice Pod URL:
`IPAddress/api/config`
The configuration API is focused on setting and reading configuration settings that are available in the Configuration Panel and the Solstice dashboard. These are admin settings that are concerned with customization, security, and network configuration options.

The top level keys are primarily associated with device-specific settings and are not grouped into a sub-hierarchy. For each table, other than the ‘Top Level’ table that does not require a hierarchical key, the hierarchical key is shown in the first row. This is the key to the set of values that can be set in that table.

## Product/Global Settings

`(Top Level)`
| Key | Type | Get/Post | Description
|:--- | :---: | :---: | :----------------------- |
| `m_displayld` | string | Get | This is the unique identifier that Solstice uses to manage a single instance, regardless of how the display is named or its current IP Address |
| `m_serverVersion` |  string | Get |  The current software version running on the Solstice Pod |
| `m_productName` | string | Get | The name of the Solstice software (Solstice). |
| `m_productVariant` | string | Get | The generation and type of Pod hardware as a name. For example, ‘Gen1’ or ‘Gen2’ |
| `m_productHardwareVersion` | int | Get | The Pod hardware generation as a version number (Pod-only). For example, 1 or 2. Software returns 9999. |

## Solstice Display Communications Settings

`m_displayInformation`

| Key | Type | Get/Post | Description
|:--- | :---: | :---: | :----------------------- |
| `m_ipv4` | string | Get | The current primary IP Address assigned to the Solstice display/endpoint. |
| `m_displayName` | string | Get/Post | The display name used for Solstice discovery. This name is shown on the Solstice splash-screen and appears in the client discovery list for connecting to the Solstice display. |
| `m_hostName` | string | Get/Post | The Solstice Pod device’s current hostname. |
| `m_port` | int | Get/Post | The base port that Solstice will use for TCP/IP communications. Solstice uses three ports defined by the base port value, +1, and +2. |

## Global Display Settings

`m_generalCuration`
| Key | Type | Get/Post | Description
|:--- | :---: | :---: | :----------------------- |
| language | string | Get/Post | Acode that denotes the current language setting. Valid options are: “en_US” for US English, “ja_JP” for Japanese, “de_DE” for German, “fr_FR” for French, “es_ES” for Spanish, “zh_TW” for Traditional Chinese, and “xx”. |
| showSplashScreen | bool | Get | Show or hide the splash screen background image when the splashscreen is visible. |
| localConfigEnabled | bool | Get | Enable or disable access to the local Configuration Panel on the Solstice Pod (via mouse/keyboard). When disabled the onscreen configuration menu is no longer visible to users. |
| browserConfigEnabled | bool | Get | If this is disabled, the API cannot interact with the host since the device considers the API browser configuration. |
| autoConnectOnClientLaunch | bool | Get/Post Enable or disable quick-connect auto launch. |
| hideOnLastClientDisconnect | bool | Get | Windows Only - hide the display software if no connections are active. |
| launchOnClientConnect | bool | Get | Windows Only - bring display software to foreground when a connection is made. |
| launchOnSystemStart | bool | Get | Windows Only - start display software when host machine boots. |
| theme | int | Get | Windows Only - selects between the 6 preset themes. Zero indexed, so the options are 0-5. |
| advancedRenderingEnabled | bool | Get/Post | Windows Only - enable (1) or disable (0) advanced rendering for better animations at the expense of host processing cycles. |
| hdmiOutDisplayMode | int | Post | Gen3 Pods Only - Change the dual display mode to Mirror (1), Seamless Extend (2}, or Extend (3}. |
| inkEnabled | bool | Post | Enable or disable support for Solstice Ink. |
| windowMode | int | Get | Windows Only - shows whether Solstice is displayed as window app (0), fixed size (1), or fullscreen (2). |
| windowTop | int | Get | Windows Only - if windowMode = 1, this is the top coordinate for the fixed window. |
| windowLeft | int | Get | Windows Only - if windowMode = 1, this is the left coordinate for the fixed window. |
| windowWidth | int | Get | Windows Only - if windowMode = 1, this is the width in pixels of the fixed window. |
| windowHeight | int | Get | Windows Only - if windowMode = 1, this is the height in pixels of the fixed window. |

## Authentication Modes

`m_authenticationCuration`
| Key | Type | Get/Post | Description
| :--- | :---: | :---: | :----------------------- |
| authenticationMode | int | Get | Pre 3.0 Solstice only - security on host is open (0), screen key (1), password (2), moderated (3), or select at runtime (4) |
| screenKeyEnabled | bool | Get/Post | Check whether screen is key protected |
| moderatorApprovalDisabled | bool | Get/Post | Check whether moderator mode is enabled or disallowed |
| sessionKey | string | Get | The current session key currently displayed on the screen and required to be entered by clients before connecting to the display |

## Main Network and Feature Record

The m_networkCuration object contains several nested sub-objects. Some of these sub-objects, including wifiConfig, apConfig, and ethernet, must have all of their properties sent in the same POST request to correctly reconfigure the Pod.

An example of how to change the nested wifiConfig sub-object is to first load the object with GET /api/config, then copy config[‘m_networkCuration’][‘wifiConfig’] into a new configuration object, then set the property changes. You must always set the password. If no password is set, the API will set the password as a single asterisk “*” to protect it.

m_networkCuration
| Key | Type | Get/Post | Description
| :--- | :---: | :---: | :----------------------- |
| connectionShowFlags | Bitwise flags (post as decimal int) | Get/Post | Bitwise flags for showing various connection related information on the Solstice splash-screen. Before posting, you will need to convert the desired bit flag into an integer. After posting, the resulting GET may include leading 1's due to the JSON parser converting it to a 32-bit integer before displaying it back.<br></br><br>NOTE: The modern splash screen only supports bits 4 through 8.</br><br>Pod only. Windows Software returns 32 ‘1’s</br><br></br><table><tr><td>Bit 1:</td><td>Main Screen - Display Name Enabled</td></tr><tr><td>Bit 2:</td><td>(Nothing)</td></tr><tr><td>Bit 3:</td><td>Main Screen - Show IP Address</td></tr><tr><td>Bit 4:</td><td>Presence Bar - Display Name</td></tr><tr><td>Bit 5:</td><td>Presence Bar - IP Address</td></tr><tr><td>Bit 6:</td><td>Main Screen - Show Screen Key</td></tr><tr><td>Bit 7:</td><td>Presence Bar - Screen Key</td></tr><tr><td>Bit 8:</td><td>Main Screen - Show Presence Bar</td></tr><tr><td>Bit 9:</td><td>Main Screen - Connect by App Instructions</td></tr><tr><td>Bit 10:</td><td>Main Screen - App Instructions - Artwork/Icons</td></tr><tr><td>Bit 11:</td><td>Main Screen - Connect by Web Instructions</td></tr><tr><td>Bit 12:</td><td>Main Screen - Web Instructions - Artwork/Icons</td></tr><tr><td>Bit 13:</td><td>Main Screen - Show SSID Info (when enabled)</td></tr></table> |
| discoveryBroadcastEnabled | bool | Get/Post | Enable or Disable UDP Discovery broadcast. When enabled the Solstice Pod will broadcast discovery information on local network every 5 seconds allowing clients to discover and connect. |
| publishToNameServer | bool | Get/Post | Publish discovery information to Solstice Discovery Service so clients can discover the Solstice Pod withoutthe need for broadcast traffic/discovery. |
| maximumConnections | int | Get/Post | The current number of maximum allowable simultaneous connections. Cannot be set past maximum allowable based on license for host. |
| maximumLicensedConnections | int | Get | Number of maximum allowable simultaneous connections based on the installed license. |
| maximumImageSize | int | Get/Post | Maximum size of an image, in bytes, shared by clients. Clients that share images past the maximum will automatically be resized (to save resources). |
| maximumPublished | int | Get/Post | Maximum number of posts allowed. Users who post past this limit will be given a message that the system is busy. |
| maximumAirPlayUsers | int | Get/Post | Maximum number of simultaneous AirPlay users allowed (ie iOS mirroring posts). Cannot be set higher than 4. |
| sdsHostName | string | Get/Post | Primary hostname or IP Address of Solstice Discovery Service to list discovery information. |
| sdsHostName2 | string | Get/Post | Secondary hostname or IP Address of Solstice Discovery Service to list discovery information. |
| remoteViewMode | int | Get/Post | Enable or disable Browser Look-In feature. 0=disabled, 1=enabled, 2=allow users to toggle on/off at runtime. Passing a value other than 0,1, or 2 disables look-in. |
| firewallMode | int | Get/Post | Modifies Dual-Network firewall (Pod only) to enable or disable internet traffic between two network interfaces. 0=Block all traffic, 1=Allow ports 80/443, 2=Allow all traffic to be ported (note: admin password must be set and sent with the request). |
| vlansEnabled | bool | Get | See if VLANs are enabled or disabled. For more information on how to set configurations, see VLANs. |
| postTypeDesktopSupported | bool | Get/Post | Enable or disable support for PC/desktop full screen sharing. |
| postTypeApplicationWindowSupported | bool | Get/Post | Enable or disable support for application window sharing. |
| postTypeMediaFilesSupported | bool | Get/Post | Enable or disable support for image and video file sharing. |
| postTypeAirPlaySupported | bool | Get/Post | Enable or disable support for iOS mirroring. |
| postTypeAndroidMirroringSupported | bool | Get/Post | Enable or disable support for Android full screen mirroring. |
| bonjourProxyEnabled | bool | Get/Post | Enable or disable the Bonjour Proxy feature that allows iOS users to discover display to mirror to via the Solstice App instead of the Bonjour protocol. |
| ethernetEnabled | bool | Get/Post | Enable or disable the Ethernet network adapter (Pod- only). |
| ethernetGatewayCheckEnabled | bool | Get/Post | Enable or disable the gateway check (Pod-only). |
| wifiMode | int | Get/Post | Set the wireless network adaptor mode 0 = Off, 1 = Client Mode/Attach to existing wireless, 2= Wireless Access Point, 3 = Wireless Miracast. |
| wifiAllowAdmin | bool | Get/Post | Enable or disable administrative access to Solstice configurations on the wireless network. |
| localOTAEnabled | bool | Get/Post | Enable or disable Solstice locating software updates using a local web server. Useful when Pods don’t have direct or web proxy-based access to the Mersive web server for updates. The localOTAUrl value is used for the URL that would be used to find the updates. Learn more about Local OTA here. |
| localOTAUrl | string | Get/Post | URL of the local web server and path to use when localOTAEnabled = true (localOTAUrl is ignored if localOTAEnabled = false). Useful when Pods don’t have direct or web proxy-based access to the Mersive web server for updates. |
| bulletinEnabled | bool | Get/Post | Enable or disable bulletin text across top of Solstice- enabled Display |
| bulletinText | string | Get/Post | Text to be displayed in bulletin |
| emergencyEnabled | bool | Get/Post | Enable or disable the emergency broadcast |
| emergencyText | bool | Get/Post | Text of emergency broadcast |
| **wifiConfig (Pod only)** | | |
| ssid | string | Get/Post | SSID of the host wireless network to connect to via wireless client mode. |
| security | int | Get/Post | Security protocol of the Pod wireless network (Pod- only). 0=open, 1=WEP, 2=WPA, 3=WPA2, 4=EAP |
| eap | int | Get/Post | EAP method of authentication when in EAP mode (Pod- only). 0=None, 1=PEAP, 2=TLS, 3=TTLS, 4=PWD, 5=SIM, 6=SIM |
| phase2 | int | Get/Post | Phase2 authentication method. 0=None, 1=PAP, 2=MSCHAP, 3=MSCHAPv2, 4=GTC. |
| password | string | Get/Post | Password used to authenticate to host network. Get returns “*” |
| dhcp | bool | Get/Post | Enable or disable DHCP protocol on wireless interface. |
| staticIP | string | Get/Post | Static IP address to assign to device on wireless interface. |
| gateway | string | Get/Post | Wireless interface gateway. |
| prefixlength | int | Get/Post | Prefix setting for wireless interface. |
| dns1 | string | Get/Post | First DNS for wireless interface. |
| dns2 | string | Get/Post | Second DNS for wireless interface. |
| **apConfig (Pod only)** |||
| SSID | string | Get/Post | SSID for standalone wireless access point. |
| SecurityMode | int | Get/Post | Security protocol for wireless interface when in WAP mode (Pod-only). 0=open, 3=WPA2. |
| PSK | string | Get/Post | Password to use for authenticating users connecting to wireless access point. |
| **ethernet (Pod only)** |||
| dhcp | bool | Get/Post | Enable or disable DHCP for the Ethernet network interface. |
| staticIP | string | Get/Post | Static IP to assign the device’s Ethernet network interface (Pod-only). |
| gateway | string | Get/Post | Gateway IP Address for the Ethernet network interface (Pod-only). |
| prefixLength | int | Get/Post | Prefix length value (netmask, Pod-only). |
| dns1 | string | Get/Post | First DNS Server IP Address (Pod-only). |
| dns2 | string | Get/Post | Second DNS Server IP Address (Pod-only). |
| allowAdmin | bool | Get/Post | Enable or disable administrative access to Solstice configurations on the wireless network. |
| **vlans (Pod only)** |||
| label | string | Get/Post | Name of the network to be displayed on the Pod's welcome screen instructions. |
| tag | int | Get/Post | Integer between 1 and 4094 that specifies your VLAN ID. |
| enabled | bool | Get/Post | Enable or disable the VLAN settings. |
| dhcp | bool | Get/Post | Enable or disable DHCP for the Ethernet network interface. |
| staticIP | string | Get/Post | Static IP to assign the device’s Ethernet network interface (Pod-only). |
| gateway | string | Get/Post | Gateway IP Address for the Ethernet network interface (Pod-only). |
| prefixLength | int | Get/Post | Prefix length value (netmask, Pod-only). |
| dns1 | string | Get/Post | First DNS Server IP Address (Pod-only). |
| dns2 | string | Get/Post | Second DNS Server IP Address (Pod-only). |
| allowAdmin | bool | Get/Post | Enable or disable administrative access to Solstice configurations on the network. |
| **httpProxyServerSettings** |||
| enabled | bool | Get/Post | Enable or disable use of an HTTP Proxy. |
| ip | string | Get/Post | IP Address of HTTP proxy server. |
| port | int | Get/Post | Communications port of HTTP proxy server. |
| username | string | Get/Post | Username to be used when authenticating to the HTTP proxy server. |
| password | string | Get/Post | Password to be used when authenticating to the HTTP proxy server. |
| excludeLocalSubnet | bool | Get/Post | Enable or disable the setting that allows addresses on the same subnet as the Pod to bypass the proxy server. |
| **httpsProxyServerSettings** |||
| enabled | bool | Get/Post | Enable or disable use of an HTTPS Proxy. |
| ip | string | Get/Post | IP Address of HTTPS proxy server. |
| port | int | Get/Post | Communications port of HTTPS proxy server. |
| username | string | Get/Post | Username to be used when authenticating to the HTTPS proxy server. |
| password | string | Get/Post | Password to be used when authenticating to the HTTPS proxy server. |
| excludeLocalSubnet | bool | Get/Post | Enable or disable the setting that allows addresses on the same subnet as the Pod to bypass the proxy server. |

## RSS Feeds

m_networkCuration also has a nested group key ‘m_rssFeedList’ that can GET or POST an array of
messages to be displayed in the RSS feed across the top of a Solstice-enabled display. It may include
custom messages or standard RSS URLs.

For example:

```
 “m_rssFeedList”: [
{
“enabled”: true,
“name”: “Custom Message”,
“length”: 0,
“uri”: “This is a test123”
},
{
“enabled”: true,
“name”: “solstice wireless display”, “length”: 3,
“uri”: “https://www.mersive.com/go.xml” }]
```

## Forget Wireless Network

You can send a standard POST IPAddress/api/config request to forget a wireless network with the
following request body:
```
json={"disable": {"ssid":"ssid_name"} }
```
As a note, this keeps the Pod in dual network mode with the wireless settings still enabled but is not
connected to anetwork. This was implemented to increase performance for streaming via Miracast.

## Licensing

m_licenseCuration
| Key | Type | Get/Post | Description
| :--- | :---: | :---: | :----------------------- |
licenseStatus int Get O=No license; 1=Error reading license; 2=License OK; 3=License Expired
trustFlags int Get 7=fully trusted; <7 and the license isn’t trusted and must be repaired
fulfillmentType string Get “PUBLISHER ACTIVATION’ or “TRIAL”
enabled bool Get Tells whether the license on the machine is enabled (1) or disabled (0)
fulfillmentid string Get A unique numerical ID used to distinguish between different machines
entitlementld string Get activation code used to activate the license on this machine
productld string Get “Solstice”
suiteld string Get Should be blank. Internal use.
expirationDate string Get “permanent” or the date the license will expire
featureLine string Get The license string returned from the license server
numDaysToExpiration int Get 999999999 if the license is permanent, otherwise the number of days until it expires
maxUsers string Get max number of users allowed by license. eg. “Unlimited”, “4”
licensing_maxPosts int Get maximum number of posts allowed by the license type.
licensing_maxPostslsConfigurable bool Get Is the user allowed to change the value of maxPosts?
licensing_atMaxPostsReplace bool Get When the max post count is reached, should the next post replace (1) or not display (0)?
licensing_maxUsers int Get maximum users allowed (O=Unlimited)}
licensing_maxUserslsConfigurable bool Get Is the user allowed to change the value of maxUsers?
licensing_remoteViewEnabled bool Get Can remote view be enabled?
licensing_remoteViewlsConfigurable bool Get Is remote view able to be configured?
licensing_runtimeAccessControls bool Get Can users can select the runtime access (moderated, screen key, etc.}?

## Passwords

m_userGroupCuration
| Key | Type | Get/Post | Description
| :--- | :---: | :---: | :----------------------- |

adminPassword string Post Administrative password for host. Note - Get on this value will always return “unknown”.
passwordValidationEnabled bool Get/Post Enable/Disable validation of admin password using the following rules:
¢ Minimum of 8 characters.
« At least one uppercase and one lowercase character.
e At least one number or special character.


## System Settings Record

m_systemCuration
| Key | Type | Get/Post | Description
| :--- | :---: | :---: | :----------------------- |
autoDateTime bool Get/Post Enable or disable the use of an NTP time server. If disabled, date and time is set manually.
ntpServer string Get/Post Non-default NTP time server IP Address. If left blank, a default internet time server will be used when autoDateTime is true.
dateTime int Get Date and time value, represented as a 64-bit integer in milliseconds since January 1, 1970, 00:00:00 GMT.
timeZone string Get/Post Time zone code represented as a string from the set of available time zones.
timeZones string Get Array of available time zone strings. See the Valid Time Zone array Values topic.
scheduledRestartEnabled bool Get/Post Enable or disable a daily Pod restart. Restarting the pod helps refresh memory usage and maximize performance.
scheduledRestartTime string Get/Post View and set the time for the daily Pod restart. The format is “hh:mm”. Hours are 00 - 23 and minutes are 00 - 59.

## Splashscreen Commands

The background image shows on a Solstice-enabled display when no content is shared. The ‘classic’ splash
screen has a single, static image, while the ‘modern’ splash screen can have up to 6 custom images in the
carousel.

- Changing the Classic Splash Screen Image:

POST your desired file (key is “file’) to IPaddress/api/config/splashbackground as type formData. In
Postman or a similar tool, you can do this by entering the URL, selecting ‘POST’, entering ‘file’ as the key,
and changing the value type from ‘text’ to ‘file’ This will allow you to upload a file from your computer
and post it to the Solstice Pod.

Reset the background to the default image by changing the value type back to ‘text’ and entering ‘reset
default’ as the value. POST to the URL to see the change on your Solstice Pod.

- Changing the Modern Splash Screen Image(s):

There are 6 slots for custom images in the modern splash screen carousel, numbered 0-5. To upload a
new image or reset a specific image to the carousel, use the same command as the classic splash screen
appended with ‘/n’ where n is the number of the image to be changed.

For example, to upload a new image to the 4th place in the carousel, you would POST your image file to
IPaddress/api/config/splashbackground/3.

Note that you cannot remove images from the carousel via the API - that can only be done using

the dashboard. If you are only using the first 3 spots then POST ‘reset default’ to |Paddress/api/config/
splashbackground/4, the 5th location in the carousel will be populated with the default image and
added to your carousel.

## Power Management

Power management offers the ability to schedule when pods stop sending an HDMI output signal after being idle for a specified amount of time, as well as the ability to turn the HDMI signal on and off on demand.

m_powerManagementCuration
| Key | Type | Get/Post | Description
| :--- | :---: | :---: | :----------------------- |

enabled

weekdaysAllDay

weekdaysBegin

weekdaysDelayMinutes

weekdaysEnd

weekendAllDay

weekendBegin

weekendDelayMinutes

weekendEnd

Type
bool
bool

string

int

string

bool

string

int

string

Get/Post
Get/Post
Get/Post
Get/Post

Get/Post

Get/Post

Get/Post
Get/Post

Get/Post

Get/Post

Description

Enable or disable power management.

On weekdays power management applies all day.

When All Day is false, this is the hour and minute that power management
starts.

The format is “hh:mm”. Hours are 00 - 23 and minutes are 00 - 59.

On weekdays this is the number of minutes of inactivity until the Pod turns
off the display. The accepted range is 1 - 120.

When All Day is false, this is the hour and minute that power management
ends.

The format is “hh:mm”. Hours are 00 - 23 and minutes are 00 - 59.

On weekends power management applies all day.

When All Day is false, this is the hour and minute that power management
starts.

The format is “hh:mm”. Hours are 00 - 23 and minutes are 00 - 59.

On weekdays this is the number of minutes of inactivity until the Pod turns
off the display. The accepted range is 1 - 120.

When All Day is false, this is the hour and minute that power management
ends.

The format is “hh:mm”. Hours are 00 - 23 and minutes are 00 - 59.

## Power Management Commands

In addition to the standard scheduling and configuration settings, power management supports dedicated
commands for turning the HDMI output on and off.

- GET |PAddress/api/control/suspend immediately puts the Pod in standby mode.
- GET IPAddress/api/control/wake immediately wakes the Pod from standby mode.

Note that suspend commands will be ignored if the pod is actively in use, there is ascheduled meeting
within 15 minutes of the current time, or when an emergency message is being broadcast.

## HDMI Input

The hdmi_input object allows you to turn off the HDMI input port on the front of the Pod. When
hdmi_input is forced off, the Pod will ignore any device that connects to this port.

The following cURL command provides an example of how to turn off the HDMI input port:

C:\API> curl -k https://192.168.2.148/api/config/hdmi_input -d
force_off=true

{"rebootRequired":false, "restartRequired": false}

The following cURL command provides an example of how to turn on the HDMI input port:

C:\API> curl -k https://192.168.2.148/api/config/hdmi_input -d
force_off=false

{"rebootRequired":false, "restartRequired": false}

If a password is set on the Pod, use the -u option to have the cURL command prompt for the Pod's admin
password. For example, you might enter something like this:

C:\API> curl -k -u admin https://192.168.2.148/api/config/hdmi_input -d
force_off=true

Enter host password for user 'admin':
{"rebootRequired":false, "restartRequired": false}

@ The hadmi_input setting does not persist through a Pod reboot. If the Pod reboots, it will
revert back to the default setting for hdmi_input whichis force_off=false.

## Calendar API

| Solstice Pod URLs: |
| :--- |
| `IPAddress/api/calendar` |
| `IPAddress/api/calendar/set` |
| `IPAddress/api/calendar/clear` |
| `IPAddress/api/calendar/add` |
| `IPAddress/api/calendar/delete` |

The calendar API allows an admin to send scheduling information to a Solstice Pod in a fully customizable way, without tying the Pod to a specific calendar via an Exchange server.

To communicate with a Pod purely via the API, the Calendar Configuration must be enabled in the Solstice Dashboard and the Calendar Type set to ‘3rd-party only’.

There are two URLs that affect Pod endpoints when ‘3rd-party only’ is selected as Calendar Type:

- `IPAddress/api/calendar/clear`
  - requires no data. Hitting this URL clears all calendar data.
- `IPAddress/api/calendar/set`
  - lets you POST JSON data about upcoming meetings. Each POST overrides any existing calendar data, so the POST should be an array of all meeting/availability information that should show on the display.

The OpenControl API may also interact with a Microsoft Exchange calendar to integrate with an existing scheduling system. After an Exchange account is authenticated through the Dashboard (Calendar Type = Microsoft Exchange), there are two URLs that allow you to add or remove a meeting on the Exchange calendar:

- `IPAddress/api/calendar/add` requires the keys ‘start Time’ ‘endTime’ ‘title’ and ‘organizer’ to add a meeting to the Exchange calendar. A random ‘id’ key is assigned when the meeting is created and may be used to delete the meeting.

QP Although the ‘organizer’ key is required for the IPAddress/api/calendar/add call, this key
may not be applied when you POST to a Microsoft Exchange calendar.

- `IPAddress/api/calendar/delete` requires only the ‘id’ key of the meeting to be deleted from the Exchange calendar.

To read calendar data from the display regardless of calendar type, GET the URL `IPAddress/api/calendar`

Example POST Data

"calendarItems": [
{ "id": "001",
"startTime":

"organizer":

1767024030,
"endTime": 1767031230,
"title": "Engineering Review",
"Molly McNale"

},

{
"id": "002",
"startTime": 1767033000,
"endTime": 1767038400,
"title": "Plastics Lunch & Learn",
"organizer": "Greg Clyff"

}

]
## Calendar Settings

Note that, like the other values in the config object, if you do not explicitly set a value to empty (",
the empty string), then it will Keep its old value. This is important when changing to a new Exchange
configuration without a delegate or impersonation mailbox.

m_calendarCuration
| Key | Type | Get/Post | Description
| :--- | :---: | :---: | :----------------------- |

Key Type
enabled bool
calendarType int
updatelntervalSeconds int
showTitle bool
showOrganizer bool
exchangeUrl string
exchangeAuthOpt int
exchangeAcctDomain string
exchangeAcctUser string
exchangeAcctPassword string
exchangeDelegateMailbox string
exchangelmpersonationMailbox string

Get/Post
Get/Post
Get/Post
Get/Post

Get/Post
Get/Post
Get/Post
Get/Post
Get/Post
Get/Post
Get/Post
Get/Post
Get/Post

Description
Enable or disable the use of a calendar service.
0: Exchange, 2: Microsoft 365, 3: OpenControl API

Number of seconds between when the display checks for updates to
the calendar information.

Show the meeting title

Show the meeting organizer

Exchange server URL

Exchange server authentication type: 0: HTTP Basic, 1: NTLM
Exchange NTLM credentials domain.

Exchange account username.

Exchange account password.

If not using the default mailbox, this is the delegate mailbox.

If not using the default mailbox, this is the impersonation mailbox.

## Calendar Commands

calendarltems
| Key | Type | Get/Post | Description
| :--- | :---: | :---: | :----------------------- |

id string Get/Post Unique meeting ID. Used internally only, does not show up on display. Must be supplied in
‘3rd-party’ mode; automatically generated in ‘Microsoft Exchange’ mode.

startTime long int Get/Post Meeting start time in Unix epoch seconds.

endTime long int Get/Post Meeting end time in Unix epoch seconds.

title string Get/Post Title of meeting that shows up on the display if meeting names are enabled in the
Dashboard.

organizer string Get/Post Name of meeting organizer that shows up on the display if enabled in the Dashboard.


## Other APIs

### Version and Update Control API

Solstice Pod URLs:

- `IPAddress/api/version/currentversion` returns JSON containing the field ‘currentVersion’ as a string.

- `IPAddress/api/version/updateavailable` returns JSON containing the bool field ‘isUpdateAvailable’. If
this value is true, the string field ‘updateAvailableTo’ will be returned as well.
- `IPAddress/api/version/update` updates Pod to version returned as ‘updateAvailableTo’ value.

### Passing RS-232 Controls API

Solstice Pod URL: IPAddress/api/serial-passthru

The RS-232 support API allows administrators to pass RS-232 controls such as power, volume, and
input through to display monitors that support RS-232. Pods must connect to screens using a USB to
serial adapter and a null modem cable. However, not all USB/RS-232 adapters may be supported. This
functionality only works with screens that support RS-232 controls.

Administrators need to know the specific RS-232 code for the control they are trying to pass. For details
on those controls, please consult the user manual for the display.

An example of the API request:

http://<ip>/api/serial-passthru/send?data=XX

In the example above, XX is a placeholder for the characters to send. Instead of a blank space, use “+”
or “%20”. For any other non-alphanumeric character, use “%XX” where XX is the two digit hexadecimal
encoding for the character.

### Other API-Related Tasks

- If you have multiple audio devices connected to a Solstice Pod, you can use the Open Control API to
override the Pod’s default USB audio device prioritization.

### Stats API

Solstice Pod URL: |PAddress/api/stats

The stats API reports statistics about the current status of the Solstice Pod. These stats are instantaneous
and can provide third-party developers with a snapshot of activity.

@ Mersive does not currently recommend polling Solstice Pods via API more than once every

10 seconds.

### Global Stats Record

(Top Level)
Key
m_displayld

m_serverVersion
m_displaylnformation

m_displayName

m_productName

m_productVariant

m_productHardwareVersion

m_statistics
m_currentPostCount
m_currentBandwidth
m_connectedUsers

m_timeSinceLastConnectionInitialize

m_currentLiveSourceCount

Type
string

string

string

string

string
int
int
int
int
int

int

Get/Post
Get

Get

Get

Get
Get

Get

Get
Get
Get
Get

Get

Description

This is the unique identifier that Solstice uses to manage a
single instance, regardless of how the display is named or its
current IP address

The current software version running on the Solstice Pod.

The name of the display, shown on welcome screen and used for
discovery.

The name of the Solstice software (Solstice).

The generation and type of Pod hardware as a name (Pod-only).
For example, ‘Gen1’ or ‘Pod Gen2’.

The Pod hardware generation as a version number (Pod-only}.
For example, 1 or 2.

Total number of posts currently shared to the display.
Total network bandwidth being used in Mbps.
Number of currently connected users.

Time since the device last has a session initiated. Returns in
milliseconds.

Number of current live sources such as a capture card; for
Windows Display Software only.

## Command API

Solstice Pod URL: |PAddress/api/control

The Command API addresses runtime control of a Solstice Pod from a third-party application. Commands

are executed by issuing a GET to the URL that corresponds to the command to be executed. The

Command API does not make use of the JSON key/value records as the other APIs do.

Security is enforced by requiring password authentication when an administrator password is set. If an
incorrect or no password is appended to the GET when one is needed, the command is ignored.

The URLs for each of the commands and their effects are listed below:

Command URL List

URL
/api/control/clear
/api/control/boot
/api/control/reboot
/api/control/restart

/api/control/
resetkey

/api/control/suspend

/api/control/wake

Impact

Clears the display of all posts.

Boots all connected users and deletes all posts on the display. Returns display to splash-screen.

Reboots Pod as soon as command is sent.
Restarts the Solstice software without rebooting the hardware.

Replace the current screen key with a new random screen key for connection authentication.

Goes into power management mode and suspends the display.

Wakes a suspended display.

## Solstice Discovery Services (SDS) API

SDS Server URL: |PAddress/api/discover

The SDS API reports statistics about the current status of the Solstice Discovery Service directory. These
stats are instantaneous and can provide third-party developers with a snapshot of all Pods managed by
this SDS server. Note that the target IP address must be the computer with SDS installed, not a Pod or
Windows Host. While SDS may be installed on the same machine as a Windows Host, the API should

not be used to call the server while the Solstice Software is active. In the Solstice Dashboard, this the IP
address shown in the SDS tab, below the "Configure Primary SDS Host" button.

Hitting a target URL of a Solstice Pod returns a single dictionary of key:value pairs pertaining to that one
Pod. [sds]/api/discover returns an array of dictionaries, where each dictionary contains the same keys but
different values, depending on the values associated with the Pod in question. For example, sending a
‘GET’ to an SDS server with two associated Pods returns something similar to this:

{

"displays": [

"name": "Pikes Peak PC",

"id": "6cebfe86—-3998-1le7-ab88-e09467b10fb1",
"ipv4": "192.168.3.31",

"port": 53100,

"user_count": 0,

"locked": false,
“airplay_enabled": false,
"session_capable": false,

"in session": false,

"tags": []

"name": "Solstice Demo 01",

"id": "b242b840-4824-49d7-b5da-adb3a434a846",
"ipv4": "192.168.3.31",

"port": 53400,

"user_count": 0,

"locked": false,
“airplay_enabled": false,
"session_capable": false,
"in session": false,
"tags": []

## SDS Commands

display
Key

name
id
ipv4

port

user_count
locked
airplay_enabled

session_capable

in_session

tags

session_name

synced_display_ids

Type

string

string

string
int
int
bool

bool

bool

bool

array

string

array

Get/
Post

Get
Get

Get
Get

Get
Get
Get
Get

Get
Get

Get

Get

Description

Assigned name of the Solstice Pod.

This is the unique identifier that Solstice uses to manage a single instance,
regardless of how the display is named or its current IP address.

IP address of Solstice Pod.

Base port for host. The base port is always used along with the next two sequential
ports.

Number of users currently connected to the Pod.
Checks if the display is locked
Checks if AirPlay mirroring is enabled for the display.

Checks if the display is capable of starting a session. Would return ‘false’ if the host
is a Windows PC that does not have the Solstice Software actively running.

Checks if Pod is involved in an active session, defined by one or more connections.

(Only shows if display has assigned tags}. Returns array of dictionaries including
the assigned tags’ tag names (“tag_name’:string) and color (“tag_color_index”:int).
There are four colors of tag:

e¢ O=blue

¢ 1=orange
« 2=green
¢ 3=pink

Only shows if in_session=true. Returns nothing unless a session name is assigned,
such as for a Multi-Room meeting.

Only shows if in_session=true. Returns nothing unless multiple displays are synced
to the session, and then returns array of display IDs.

## Valid Time Zone Values

The currently set time zone on a device is returned from the API call “timeZone” by id. The API call
“timeZones” returns a string array of all available time zones.

ID Name Offset (ms) Offset (hrs)
Pacific/Midway GMT-11:00, Midway Island -39600000 -11
Pacific/Honolulu GMT-10:00, Hawaii -36000000 -10
America/Anchorage GMT-8:00, Alaska -28800000 -8
America/Los_Angeles GMT-7:00, Pacific Time -25200000 -7
America/Tijuana GMT-7:00, Tijuana -25200000 -7
America/Phoenix GMT-7:00, Arizona -25200000 -7
America/Chihuahua GMT-6:00, Chihuahua -21600000 -6
America/Denver GMT-6:00, Mountain Time -21600000 -6
America/Costa_Rica GMT-6:00, Central America -21600000 -6
America/Regina GMT-6:00, Saskatchewan -21600000 -6
America/Chicago GMT-5:00, Central Time -18000000 -5
America/Mexico_City GMT-5:00, Mexico City -18000000 -5
America/Bogota GMT-5:00, Bogota -18000000 5
America/Caracas GMT-4:30, Venezuela -16200000 -4.5
America/New_York GMT-4:00, Eastern Time -14400000 -4
America/Barbados GMT-4:00, Atlantic Time (Barbados) -14400000 -4
America/Manaus GMT-4:00, Manaus -14400000 -4
America/Halifax GMT-3:00, Atlantic Time (Canada) -10800000 -3
America/Santiago GMT-3:00, Santiago -10800000 -3
America/Sao_Paulo GMT-3:00, Brasilia -10800000 -3
America/Argentina/ GMT-3:00, Buenos Aires -10800000 -3
Buenos_Aires

America/Montevideo GMT-3:00, Montevideo -10800000 -3
America/St_Johns GMT-2:30, Newfoundland -9000000 -2.5
America/Godthab GMT-2:00, Greenland -7200000 -2
Atlantic/South_Georgia GMT-2:00, Mid-Atlantic -7200000 -2
Atlantic/Cape_Verde GMT-1:00, Cape Verde Islands -3600000 -1
Atlantic/Azores GMT+0:00, Azores 16) 16)
Africa/Casablanca GMT+0:00, Casablanca 16) 16)
Europe/London GMT+1:00, London, Dublin 3600000 1
Africa/Windhoek GMT+1:00, Windhoek 3600000 1
Africa/Brazzaville GMT+1:00, W. Africa Time 3600000 1
Europe/Amsterdam GMT+2:00, Amsterdam, Berlin 7200000 2
Europe/Belgrade GMT+2:00, Belgrade 7200000 2
Europe/Brussels GMT+2:00, Brussels 7200000 2
Europe/Sarajevo GMT+2:00, Sarajev 7200000 2
Africa/Cairo GMT+2:00, Cairo 7200000 2
Africa/Harare GMT+2:00, Harare 7200000 2
Asia/Amman GMT+3:00, Amman, Jordan 10800000 3


ID
Europe/Athens
Asia/Beirut
Europe/Helsinki
AsiaJerusalem
Europe/Minsk
Asia/Baghdad
Europe/Moscow
Asia/Kuwait
Africa/Nairobi
Asia/Tbilisi
Asia/Yerevan
Asia/Duba
Asia/Tehran
Asia/Kabul
Asia/Baku
Asia/Karachi
Asia/Oral
Asia/Yekaterinburg
Asia/Calcutta
Asia/Colombo
Asia/Katmandu
Asia/Almaty
Asia/Rangoon
Asia/Krasnoyarsk
Asia/Bangkok
Asia/Shanghai
Asia/Hong_Kong
Asia/Irkutsk
Asia/Kuala_Lumpur
Australia/Perth
Asia/Taipei
Asia/Seoul
Asia/Tokyo
Asia/Yakutsk
Australia/Adelaide
Australia/Darwin
Australia/Brisbane
Australia/Hobart
Australia/Sydney
Asia/Vladivostok
Pacific/Guam
Asia/Magadan
Pacific/Majuro
Pacific/Auckland
Pacific/Fiji

Name

GMT+3:00, Athens, Istanbul
GMT+3:00, Beirut, Lebanon

GMT+3:00, Helsinki
GMT+3:00, Jerusalem
GMT+3:00, Minsk
GMT+3:00, Baghdad
GMT+3:00, Moscow
GMT+3:00, Kuwait
GMT+3:00, Nairobi
GMT+4:00, Tbilisi
GMT+4:00, Yerevan
GMT+4:00, Dubai
GMT+4:30, Tehran
GMT+4:30, Kabul
GMT+5:00, Baku

GMT+5:00, Islamabad, Karachi

GMT+5:00, Ural\sk

GMT+5:00, Yekaterinburg

GMT+5:30, Kolkata
GMT+5:30, Sri Lanka
GMT+5:45, Kathmandu
GMT+6:00, Astana
GMT+6:30, Yangon
GMT+7:00, Krasnoyarsk
GMT+7:00, Bangkok
GMT+8:00, Beijing
GMT+8:00, Hong Kong
GMT+8:00, Irkutsk

GMT+8:00, Kuala Lumpur

GMT+8:00, Perth
GMT+8:00, Taipei
GMT+9:00, Seoul
GMT+9:00, Tokyo, Osaka
GMT+9:00, Yakutsk
GMT+9:30, Adelaide
GMT+9:30, Darwin
GMT+10:00, Brisbane
GMT+10:00, Hobart

GMT+10:00, Sydney, Canberra

GMT+10:00, Vladivostok
GMT+10:00, Guam
GMT+10:00, Magadan

GMT+12:00, Marshall Islands

GMT+12:00, Auckland
GMT+12:00, Fiji

Offset (ms)
10800000
10800000
10800000
10800000
10800000
10800000
10800000
10800000
10800000
14400000
14400000
14400000
16200000
16200000
18000000
18000000
18000000
18000000
19800000
19800000
20700000
21600000
23400000
25200000
25200000
28800000
28800000
28800000
28800000
28800000
28800000
32400000
32400000
32400000
34200000
34200000
36000000
36000000
36000000
36000000
36000000
36000000
43200000
43200000
43200000

Offset (hrs)

a oH

Oo OO OO OO oO NS

95
10
10
10
10
10
10
12
12
12

ID Name
Pacific/Tongatapu GMT+13:00, Tonga

Offset (ms)
46800000

Offset (hrs)
13
