# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM


from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from app.translate import translate
from app.my_yhzlearn import bp


@bp.route('/yhz1', methods=['get', 'POST'])
def yhz1():
    return render_template('my_yhzlearn/yhz1.html')
    # return "hahahahahah"

