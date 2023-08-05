# stopeight: Comparing sequences of points in 2 dimensions.
# Copyright (C) 2009-2016 Specific Purpose Software GmbH
# Copyright (C) 2017-2018 Fassio Blatter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; NO OTHER VERSION than version 2.0 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

#When Python2 support is droped, remove this pkgutil-style file for native python3 namespaces
__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from stopeight.logging import logSwitch
# Note: This is done once at module import
logSwitch.initialize_config()
