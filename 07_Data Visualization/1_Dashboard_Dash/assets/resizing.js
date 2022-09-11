# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 13:04:28 2022

@author: cflorelu
"""

/* resize figures in table upon callback get fires */

if(!window.dash_clientside) {window.dash_clientside = {};}
window.dash_clientside.clientside = {
   resize: function (value) {
       console.log("resizing...");
       window.dispatchEvent(new Event('resize'));
       return null
   }
}