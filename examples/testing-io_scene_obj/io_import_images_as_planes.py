# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {
    "name": "Import Images as Planes",
    "author": "Florian Meyer (tstscr), mont29, matali, Ted Schundler (SpkyElctrc)",
    "version": (3, 3, 0),
    "blender": (2, 80, 0),
    "location": "File > Import > Images as Planes or Add > Mesh > Images as Planes",
    "description": "Imports images and creates planes with the appropriate aspect ratio. "
                   "The images are mapped to the planes.",
    "warning": "",
    "doc_url": "{BLENDER_MANUAL_URL}/addons/import_export/images_as_planes.html",
    "support": 'OFFICIAL',
    "category": "Import-Export",
}

def register():
    print("Hello World")


def unregister(): # pragma: no cover
    print("Goodbye World") 
