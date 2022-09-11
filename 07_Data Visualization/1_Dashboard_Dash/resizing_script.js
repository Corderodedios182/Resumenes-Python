# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 13:20:41 2022

@author: cflorelu
"""

if (!window.dash_clientside) {
  window.dash_clientside = {};
}
window.dash_clientside.clientside = {
  resize: function(value) {
    console.log("resizing..."); // for testing
    setTimeout(function() {
      window.dispatchEvent(new Event("resize"));
      console.log("fired resize");
    }, 500);
    return null;
  }
};