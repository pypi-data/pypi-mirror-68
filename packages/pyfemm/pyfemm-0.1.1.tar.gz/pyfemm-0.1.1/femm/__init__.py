import win32com.client 
import os
from six import string_types

def fixpath(myPath):
	return myPath.replace('\\','/').replace('//','/')
	
def openfemm(*arg):
	global HandleToFEMM
	HandleToFEMM = win32com.client.Dispatch( "femm.ActiveFEMM")
	callfemm('setcurrentdirectory(' + quote(fixpath(os.getcwd())) + ')' );
	if len(arg) == 0 :
		main_restore()
		return;
	if arg[0]==0 :
		main_restore()
		return;
		
def closefemm():
	global HandleToFEMM
	del HandleToFEMM	
	
def callfemm(myString):
	global HandleToFEMM
	x = HandleToFEMM.mlab2femm(myString).replace("[ ","[").replace(" ]","]").replace(" ",",").replace("I","1j");
	if len(x)==0: 
		x=[]
	elif x[0] =='e' :
		ErrorMsg=x.replace(","," ").replace("1j","I")
		raise Exception(ErrorMsg)
	else:
		x=eval(x)
	if len(x)==1:
		x=x[0];
	return x;
	
def main_restore():
	callfemm("main_restore()")

def num(n):
	return str(n).replace('j','*I')
	
def numc(n):
	return num(n) + ","

def quote(myString):
	return '"' + myString + '"';

def quotec(myString):
	return '"' + myString + '",';
	
def doargs(*arg):
	if len(arg)==0:
		return '()'
	x='(';
	for k in range(0,len(arg)):
		y=arg[k];
		if isinstance(y, string_types):
			x = x + '"' + y + '"';
		else:
			x = x + str(y);
		if k == (len(arg)-1):
			x = x + ')';
		else:
			x = x + ',';
	return x
	
def newdocument(k):
	callfemm("newdocument(" + num(k) + ")");
	
def AWG(awg) :
	return 8.2514694*exp(-0.115943*awg);

def callfemm_noeval(myString):
	global HandleToFEMM
	HandleToFEMM.mlab2femm(myString)

def ci_addarc(*arg):
	callfemm('ci_addarc' + doargs(*arg))

def ci_addblocklabel(*arg):
	callfemm('ci_addblocklabel' + doargs(*arg))

def ci_addboundprop(*arg):
	callfemm('ci_addboundprop' + doargs(*arg));

def ci_addconductorprop(*arg):
	callfemm('ci_addconductorprop' + doargs(*arg))

def ci_addmaterial(*arg):
	callfemm('ci_addmaterial' + doargs(*arg))

def ci_addnode(*arg):
    callfemm('ci_addnode' + doargs(*arg))

def ci_addpointprop(*arg):
	callfemm('ci_addpointprop' + doargs(*arg))

def ci_addsegment(*arg):
	callfemm('ci_addsegment' + doargs(*arg))

def ci_analyze(*arg):
	callfemm('ci_analyze' + doargs(*arg))

def ci_analyse(n):
	ci_analyze(n)
	
def ci_attachdefault():
	callfemm('ci_attachdefault()');

def ci_clearselected():
	callfemm('ci_clearselected()');

def ci_cleartkpoints(n):
	callfemm('ci_cleartkpoints(' + quote(n) + ')' );

def ci_close():
	callfemm('ci_close()');

def ci_copyrotate(*arg):
	callfemm('ci_copyrotate' + doargs(*arg))

def ci_copyrotate2(*arg):
	callfemm('ci_copyrotate' + doargs(*arg))

def ci_copytranslate(*arg):
	callfemm('ci_copytranslate' + doargs(*arg))

def ci_createmesh():
	return callfemm('ci_createmesh()');

def ci_createradius(x,y,r):
	callfemm('ci_createradius(' + numc(x) + numc(y)+ num(r) + ')' );

def ci_deleteboundprop(n):
	callfemm('ci_deleteboundprop(' + quote(n) + ')' );

def ci_deleteconductor(n):
	callfemm('ci_deleteconductor(' + quote(n) + ')' );

def ci_deletematerial(n):
	callfemm('ci_deletematerial(' + quote(n) + ')' );

def ci_deletepointprop(n):
	callfemm('ci_deletepointprop(' + quote(n) + ')' );

def ci_deleteselected():
	callfemm('ci_deleteselected()');

def ci_deleteselectedarcsegments():
	callfemm('ci_deleteselectedarcsegments()');
	
def ci_deleteselectedlabels():
	callfemm('ci_deleteselectedlabels()');

def ci_deleteselectednodes():
	callfemm('ci_deleteselectednodes()');

def ci_deleteselectedsegments():
	callfemm('ci_deleteselectedsegments()');

def ci_detachdefault():
	callfemm('ci_detachdefault()');

def ci_drawarc(x1,y1,x2,y2,angle,maxseg):
	ci_addnode(x1,y1);
	ci_addnode(x2,y2);
	ci_addarc(x1,y1,x2,y2,angle,maxseg);

def ci_drawline(x1,y1,x2,y2):
	ci_addnode(x1,y1);
	ci_addnode(x2,y2);
	ci_addsegment(x1,y1,x2,y2);

def ci_drawrectangle(x1,y1,x2,y2):
	ci_drawline(x1,y1,x2,y1);
	ci_drawline(x2,y1,x2,y2);
	ci_drawline(x2,y2,x1,y2);
	ci_drawline(x1,y2,x1,y1);

def ci_getmaterial(matname):
	callfemm('ci_getmaterial(' + quote(matname) + ')' );

def ci_hidegrid():
	callfemm('ci_hidegrid()');

def ci_hidenames():
	callfemm('ci_shownames(0)');

def ci_loadsolution():
	callfemm('ci_loadsolution()');

def ci_makeABC(*args):
	callfemm('ci_makeABC' + doargs(*arg))

def ci_maximize():
	callfemm('ci_maximize()');

def ci_minimize():
	callfemm('ci_minimize()');

def ci_mirror(x1,x2,y1,y2):
	callfemm('ci_mirror(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );

def ci_mirror2(x1,x2,y1,y2,editaction):
	callfemm('ci_mirror(' + numc(x1) + numc(y1) + numc(x2) + numc(y2) + num(editaction) + ')' );

def ci_modifyboundprop(*arg):
	callfemm('ci_modifyboundprop' + doargs(*arg));

def ci_modifyconductorprop(*arg):
	callfemm('ci_modifyconductorprop' + doargs(*arg));
	
def ci_modifymaterial(*arg):
	callfemm('ci_modifymaterial' + doargs(*arg))
	
def ci_modifypointprop(*arg):
	callfemm('ci_modifypointprop' + doargs(*arg))

def ci_moverotate(bx,by,shiftangle):
	callfemm('ci_moverotate(' + numc(bx) + numc(by) + num(shiftangle) + ')' );

def ci_movetranslate(bx,by):
	callfemm('ci_movetranslate(' + numc(bx) + num(by) + ')' );

def ci_movetranslate2(bx,by,editaction):
	callfemm('ci_movetranslate(' + numc(bx) + numc(by) + num(editaction) + ')' );

def ci_probdef(*arg):
	callfemm('ci_probdef' + doargs(*arg))

def ci_purgemesh():
	callfemm('ci_purgemesh()');

def ci_readdxf(docname):
	callfemm('print(ci_readdxf(' + quote(docname) + '))' );

def ci_refreshview():
	callfemm('ci_refreshview()');

def ci_resize(nWidth,nHeight):
	callfemm('ci_resize('+ numc(nWidth)+ num(nHeight)+ ')' );

def ci_restore():
	callfemm('ci_restore()');

def ci_saveas(fn):
	callfemm('ci_saveas(' + quote(fixpath(fn)) + ')');

def ci_savebitmap(n):
	callfemm('ci_savebitmap(' + quote(n) + ')' );

def ci_savedxf(docname):
	callfemm_noeval('ci_savedxf(' + quote(docname) + ')' );

def ci_savemetafile(n):
	callfemm('ci_savemetafile(' + quote(n) + ')' );

def ci_scale(bx,by,sc):	
	callfemm('ci_scale(' + numc(bx) + numc(by) + numc(sc) + ')' );

def ci_scale2(bx,by,sc,ea):
	callfemm('ci_scale(' + numc(bx) + numc(by) + numc(sc) + num(ea) + ')' );

def ci_selectarcsegment(x,y):
	return callfemm('ci_selectarcsegment(' + numc(x) + num(y) + ')');
 
def ci_selectcircle(*arg):
	return callfemm('ci_selectcircle' + doargs(*arg))

def ci_selectgroup(gr):
	return callfemm('ci_selectgroup(' + num(gr) + ')' );

def ci_selectlabel(x,y):
	return callfemm('ci_selectlabel(' + numc(x) + num(y) + ')');

def ci_selectnode(x,y):
	return callfemm('ci_selectnode(' + numc(x) + num(y) + ')');

def ci_selectrectangle(*arg):
	callfemm('ci_selectrectangle' + doargs(*arg))

def ci_selectsegment(x,y):
	return callfemm('ci_selectsegment(' + numc(x) + num(y) + ')');

def ci_setarcsegmentprop(maxsegdeg,propname,hide,group,incond):
	callfemm('ci_setarcsegmentprop(' + numc(maxsegdeg) + quotec(propname) + numc(hide) + numc(group) + quote(incond) + ')' );

def ci_setblockprop(blockname,automesh,meshsize,group):
	callfemm('ci_setblockprop(' + quotec(blockname) + numc(automesh) + numc(meshsize) + num(group) + ')');

def ci_seteditmode(editmode):
	callfemm('ci_seteditmode(' + quote(editmode) + ')' );

def ci_setfocus(docname):
	callfemm('ci_setfocus(' + quote(docname) + ')' );

def ci_setgrid(density,ptype):
	callfemm('ci_setgrid(' + numc(density) + quote(ptype) + ')' );

def ci_setgroup(n):
	return callfemm('ci_setgroup(' + num(n) + ')' );

def ci_setnodeprop(nodeprop,groupno,incond):
	callfemm('ci_setnodeprop(' + quotec(nodeprop) + numc(groupno) + quote(inconductor) + ')');

def ci_setsegmentprop(pn,es,am,hi,gr, incond):
	callfemm('ci_setsegmentprop(' + quotec(pn) + numc(es) + numc(am) + numc(hi) + numc(gr) + quote(incond) + ')');

def ci_showgrid():
	callfemm('ci_showgrid()');

def ci_showmesh():
	callfemm('ci_showmesh()');

def ci_shownames():
	callfemm('ci_shownames(1)');

def ci_smartmesh(n):
	callfemm('ci_smartmesh(' + num(n)+ ')' );

def ci_snapgridoff():
	callfemm('ci_gridsnap("off")');

def ci_snapgridon():
	callfemm('ci_gridsnap("on")');

def ci_zoom(x1,y1,x2,y2):
	callfemm('ci_zoom(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );

def ci_zoomin():
	callfemm('ci_zoomin()');

def ci_zoomnatural():
	callfemm('ci_zoomnatural()');

def ci_zoomout():
	callfemm('ci_zoomout()');

def co_addcontour(x,y):
	callfemm('co_addcontour(' + numc(x) + num(y) + ')' );

def co_bendcontour(tta,dtta):
	callfemm('co_bendcontour(' + numc(tta) + num(dtta) + ')' );

def co_blockintegral(ptype):
	return callfemm('co_blockintegral(' + num(ptype) + ')' );

def co_clearblock():
	callfemm('co_clearblock()');

def co_clearcontour():
	callfemm('co_clearcontour()');

def co_close():
	callfemm('co_close()');

def co_getconductorproperties(pname):
	return callfemm('co_getconductorproperties(' + quote(pname) + ')' );

def co_gete(x,y):
	z=co_getpointvalues(x,y)
	return [z[5],z[6]]

def co_getelement(n):
	return callfemm('co_getelement(' + num(n) + ')' );

def co_getj(x,y):
	z=co_getpointvalues(x,y)
	return [z[1],z[2]]

def co_getk(x,y):
	z=co_getpointvalues(x,y)
	return [z[3],z[4]]

def co_getnode(n):
	return callfemm('co_getnode(' + num(n) + ')' );

def co_getpointvalues(x,y):
	return callfemm('co_getpointvalues(' + numc(x) + num(y) + ')' );

def co_getprobleminfo():
	return callfemm('co_getprobleminfo()');

def co_getv(x,y):
	z=co_getpointvalues(x,y)
	return z[0]

def co_groupselectblock(*arg):
	callfemm('co_groupselectblock' + doargs(*arg))

def co_hidecontourplot():
	callfemm('co_hidecontourplot()');

def co_hidedensityplot():
	callfemm('co_hidedensityplot()');

def co_hidegrid():
	callfemm('co_hidegrid()');

def co_hidemesh():
	callfemm('co_hidemesh()');

def co_hidenames():
	callfemm('co_shownames(0)');

def co_hidepoints():
	callfemm('co_hidepoints()');

def co_lineintegral(ptype):
	return callfemm('co_lineintegral(' + num(ptype) + ')' );

def co_makeplot(*arg):
	callfemm('co_makeplot' + doargs(*arg))

def co_maximize():
	callfemm('co_maximize()');

def co_minimize():
	callfemm('co_minimize()');

def co_numelements():
	return callfemm('co_numelements()');

def co_numnodes():
	return callfemm('co_numnodes()');

def co_refreshview():
	callfemm('co_refreshview()');

def co_reload():
	callfemm('co_reload()');

def co_resize(nWidth,nHeight):
	callfemm('co_resize('+ numc(nWidth)+ num(nHeight)+ ')' );

def co_restore():
	callfemm('co_restore()');

def co_savebitmap(fn):
	callfemm('co_savebitmap(' + quote(fixpath(fn)) + ')' );

def co_savemetafile(fn):
	callfemm('co_savemetafile(' + quote(fixpath(fn)) + ')' );

def co_selectblock(x,y):
	callfemm('co_selectblock(' + numc(x) + num(y) + ')' )

def co_selectpoint(x,y):
	callfemm('co_selectpoint(' + numc(x) + num(y) + ')' )

def co_seteditmode(mode):
	callfemm('co_seteditmode(' + quote(mode) + ')' );

def co_setgrid(density,ptype):
	callfemm('co_setgrid(' + numc(density) + quote(ptype) + ')' );

def co_showcontourplot(numcontours,al,au):
	callfemm('co_showcontourplot(' + numc(numcontours) + numc(al) + num(au) + ')' );

def co_showdensityplot(legend,gscale,ptype,bu,bl):
	callfemm('co_showdensityplot(' + numc(legend) + numc(gscale) + numc(ptype) + numc(bu) + num(bl) + ')' );

def co_showgrid():
	callfemm('co_showgrid()');

def co_showmesh():
	callfemm('co_showmesh()');

def co_shownames():
	callfemm('co_shownames(1)');

def co_showpoints():
	callfemm('co_showpoints()');

def co_showvectorplot(*arg):
	callfemm('co_showvectorplot' + doargs(*arg))

def co_smooth(flag):
	callfemm('co_smooth(' + quote(flag) + ')' );

def co_smoothoff():
	callfemm('co_smooth("off")');

def co_smoothon():
	callfemm('co_smooth("on")');

def co_snapgrid(flag):
	callfemm('co_gridsnap(' + quote(flag) + ')' );

def co_snapgridoff():
	callfemm('co_gridsnap("off")');

def co_snapgridon():
	callfemm('co_gridsnap("on")');

def co_zoom(x1,y1,x2,y2):
	callfemm('co_zoom(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );

def co_zoomin():
	callfemm('co_zoomin()');

def co_zoomnatural():
	callfemm('co_zoomnatural()');

def co_zoomout():
	callfemm('co_zoomout()');

def complex2str(x):
	return str(x)
	
def create(n):
	callfemm( 'create(' + num(n) + ')' );

def ei_addarc(x1,y1,x2,y2,angle,maxseg):
	callfemm('ei_addarc(' + numc(x1) + numc(y1) + numc(x2) + numc(y2) + numc(angle) + num(maxseg) + ')');

def ei_addblocklabel(x,y):
	callfemm('ei_addblocklabel(' + numc(x) + num(y) + ')' );

def ei_addboundprop(pname,vs,qs,c0,c1,fmt):
	callfemm('ei_addboundprop(' + quotec(pname) + numc(vs) + numc(qs) + numc(c0) + numc(c1) + num(fmt) + ')' );

def ei_addconductorprop(pname,vc,qc,ptype):
	callfemm('ei_addconductorprop(' + quotec(pname) + numc(vc) + numc(qc) + num(ptype) + ')' );

def ei_addmaterial(pname,ex,ey,qv):
	callfemm('ei_addmaterial(' + quotec(pname) + numc(ex) + numc(ey) + num(qv) + ')' );

def ei_addnode(x,y):
	callfemm('ei_addnode(' + numc(x) + num(y) + ')');

def ei_addpointprop(pname,vp,qp):
	callfemm('ei_addpointprop(' + quotec(pname) + numc(vp) + num(qp) + ')');

def ei_addsegment(x1,y1,x2,y2):
	callfemm('ei_addsegment(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );

def ei_analyze(*arg):
	callfemm('ei_analyze' + doargs(*arg))

def ei_analyse(n):
	ei_analyze(n)

def ei_attachdefault():
	callfemm('ei_attachdefault()');

def ei_attachouterspace():
	callfemm('ei_attachouterspace()');

def ei_clearselected():
	callfemm('ei_clearselected()');

def ei_close():
	callfemm('ei_close()');

def ei_copyrotate(bx,by,angle,copies):
	callfemm('ei_copyrotate(' + numc(bx) + numc(by) + numc(angle) + num(copies) + ')' );

def ei_copyrotate2(bx,by,angle,copies,editaction):
	callfemm('ei_copyrotate(' + numc(bx) + numc(by) + numc(angle) + numc(copies) + num(editaction) + ')' );

def ei_copytranslate(bx,by,copies):
	callfemm('ei_copytranslate(' + numc(bx) + numc(by) + num(copies) + ')' );

def ei_copytranslate2(bx,by,copies,editaction):
	callfemm('ei_copytranslate(' + numc(bx) + numc(by) + numc(copies) + num(editaction) + ')' );

def ei_createmesh():
	return callfemm('ei_createmesh()');

def ei_createradius(x,y,r):
	callfemm('ei_createradius(' + numc(x) + numc(y)+ num(r) + ')' );

def ei_defineouterspace(Zo,Ro,Ri):
	callfemm('ei_defineouterspace(' + numc(Zo) + numc(Ro) + num(Ri) + ')' );

def ei_deleteboundprop(n):
	callfemm('ei_deleteboundprop(' + quote(n) + ')' );

def ei_deleteconductor(n):
	callfemm('ei_deleteconductor(' + quote(n) + ')' );

def ei_deletematerial(n):
	callfemm('ei_deletematerial(' + quote(n) + ')' );

def ei_deletepointprop(n):
	callfemm('ei_deletepointprop(' + quote(n) + ')' );

def ei_deleteselected():
	callfemm('ei_deleteselected()');

def ei_deleteselectedarcsegments():
	callfemm('ei_deleteselectedarcsegments()');

def ei_deleteselectedlabels():
	callfemm('ei_deleteselectedlabels()');

def ei_deleteselectednodes():
	callfemm('ei_deleteselectednodes()');

def ei_deleteselectedsegments():
	callfemm('ei_deleteselectedsegments()');

def ei_detachdefault():
	callfemm('ei_detachdefault()');

def ei_detachouterspace():
	callfemm('ei_detachouterspace()');

def ei_drawarc(x1,y1,x2,y2,angle,maxseg):
	ei_addnode(x1,y1);
	ei_addnode(x2,y2);
	ei_addarc(x1,y1,x2,y2,angle,maxseg);

def ei_drawline(x1,y1,x2,y2):
	ei_addnode(x1,y1);
	ei_addnode(x2,y2);
	ei_addsegment(x1,y1,x2,y2);

def ei_drawrectangle(x1,y1,x2,y2):
	ei_drawline(x1,y1,x2,y1);
	ei_drawline(x2,y1,x2,y2);
	ei_drawline(x2,y2,x1,y2);
	ei_drawline(x1,y2,x1,y1);

def ei_getmaterial(matname):
	callfemm('ei_getmaterial(' + quote(matname) + ')' );

def ei_hidegrid():
	callfemm('ei_hidegrid()');

def ei_hidenames():
	callfemm('ei_shownames(0)');

def ei_loadsolution():
	callfemm('ei_loadsolution()');

def ei_makeABC(*arg):
	callfemm('ei_makeABC' + doargs(*arg))

def ei_maximize():
	callfemm('ei_maximize()');

def ei_minimize():
	callfemm('ei_minimize()');

def ei_mirror(x1,y1,x2,y2):
	callfemm('ei_mirror(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );

def ei_mirror2(x1,y1,x2,y2,editaction):
	callfemm('ei_mirror(' + numc(x1) + numc(y1) + numc(x2) + numc(y2) + num(editaction) + ')' );

def ei_modifyboundprop(*arg):
	callfemm('ei_modifyboundprop' + doargs(*arg))

def ei_modifyconductorprop(*arg):
	callfemm('ei_modifyconductorprop' + doargs(*arg))

def ei_modifymaterial(*arg):
	callfemm('ei_modifymaterial' + doargs(*arg))
	
def ei_modifypointprop(*arg):
	callfemm('ei_modifypointprop' + doargs(*arg))

def ei_moverotate(bx,by,shiftangle):
	callfemm('ei_moverotate(' + numc(bx) + numc(by) + num(shiftangle) + ')' );

def ei_movetranslate(bx,by):
	callfemm('ei_movetranslate(' + numc(bx) + num(by) + ')' );

def ei_movetranslate2(bx,by,editaction):
	callfemm('ei_movetranslate(' + numc(bx) + numc(by) + num(editaction) + ')' );

def ei_probdef(*arg):
	callfemm('ei_probdef' + doargs(*arg))

def ei_purgemesh():
	callfemm('ei_purgemesh()');

def ei_readdxf(docname):
	callfemm('print(ei_readdxf(' + quote(docname) + '))' );

def ei_refreshview():
	callfemm('ei_refreshview()');

def ei_resize(nWidth,nHeight):
	callfemm('ei_resize('+ numc(nWidth)+ num(nHeight)+ ')' );

def ei_restore():
	callfemm('ei_restore()');

def ei_saveas(fn):
	callfemm('ei_saveas(' + quote(fixpath(fn)) + ')');

def ei_savebitmap(n):
	callfemm('ei_savebitmap(' + quote(n) + ')' );

def ei_savedxf(docname):
	callfemm_noeval('ei_savedxf(' + quote(docname) + ')' );

def ei_savemetafile(n):
	callfemm('ei_savemetafile(' + quote(n) + ')' );

def ei_scale(bx,by,sc):
	callfemm('ei_scale(' + numc(bx) + numc(by) + numc(sc) + ')' );

def ei_scale2(bx,by,sc,ea):
	callfemm('ei_scale(' + numc(bx) + numc(by) + numc(sc) + num(ea) + ')' );

def ei_selectarcsegment(x,y):
	return callfemm('ei_selectarcsegment(' + numc(x) + num(y) + ')'); 

def ei_selectcircle(*arg):
	callfemm('ei_selectcircle' + doargs(*arg))

def ei_selectgroup(gr):
	callfemm('ei_selectgroup(' + num(gr) + ')' );

def ei_selectlabel(x,y):
	return callfemm('ei_selectlabel(' + numc(x) + num(y) + ')');

def ei_selectnode(x,y):
	return callfemm('ei_selectnode(' + numc(x) + num(y) + ')');

def ei_selectrectangle(*arg):
	callfemm('ei_selectrectangle' + doargs(*arg))

def ei_selectsegment(x,y):
	return callfemm('ei_selectsegment(' + numc(x) + num(y) + ')');

def ei_setarcsegmentprop(maxsegdeg,propname,hide,group,incond):
	callfemm('ei_setarcsegmentprop(' + numc(maxsegdeg) + quotec(propname) + numc(hide) + numc(group) + quote(incond) + ')' );

def ei_setblockprop(blockname,automesh,meshsize,group):
	callfemm('ei_setblockprop(' + quotec(blockname) + numc(automesh) + numc(meshsize) + num(group) + ')');

def ei_seteditmode(editmode):
	callfemm('ei_seteditmode(' + quote(editmode) + ')' );

def ei_setfocus(docname):
	callfemm('ei_setfocus(' + quote(docname) + ')' );

def ei_setgrid(density,ptype):
	callfemm('ei_setgrid(' + numc(density) + quote(ptype) + ')' );

def ei_setgroup(n):
	return callfemm('ei_setgroup(' + num(n) + ')' );

def ei_setnodeprop(nodeprop,groupno,inconductor):
	callfemm('ei_setnodeprop(' + quotec(nodeprop) + numc(groupno) + quote(inconductor) + ')');

def ei_setsegmentprop(pn,es,am,hi,gr, inconductor):
	callfemm('ei_setsegmentprop(' + quotec(pn) + numc(es) + numc(am) + numc(hi) + numc(gr) + quote(inconductor) + ')');

def ei_showgrid():
	callfemm('ei_showgrid()');

def ei_showmesh():
	callfemm('ei_showmesh()');

def ei_shownames():
	callfemm('ei_shownames(1)');

def ei_smartmesh(n):
	callfemm('ei_smartmesh(' + num(n)+ ')' );

def ei_snapgridoff():
	callfemm('ei_gridsnap("off")');

def ei_snapgridon():
	callfemm('ei_gridsnap("on")');

def ei_zoom(x1,y1,x2,y2):
	callfemm('ei_zoom(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );

def ei_zoomin():
	callfemm('ei_zoomin()');

def ei_zoomnatural():
	callfemm('ei_zoomnatural()');

def ei_zoomout():
	callfemm('ei_zoomout()');

def eo_addcontour(x,y):
	callfemm('eo_addcontour(' + numc(x) + num(y) + ')' );

def eo_bendcontour(tta,dtta):
	callfemm('eo_bendcontour(' + numc(tta) + num(dtta) + ')' );

def eo_blockintegral(ptype):
	return callfemm('eo_blockintegral(' + num(ptype) + ')' );
        
def eo_clearblock():
	callfemm('eo_clearblock()');

def eo_clearcontour():
	callfemm('eo_clearcontour()');

def eo_close():
	callfemm('eo_close()');

def eo_getconductorproperties(pname):
	return callfemm('eo_getconductorproperties(' + quote(pname) + ')' );
	
def eo_getd(x,y):
	z=eo_getpointvalues(x,y);
	return [z[1],z[2]]

def eo_gete(x,y):
	z=eo_getpointvalues(x,y);
	return [z[3],z[4]]

def eo_getelement(n):
	return callfemm('eo_getelement(' + num(n) + ')' );

def eo_getenergydensity(x,y):
	z=eo_getpointvalues(x,y)
	return z[7]

def eo_getnode(n):
	return callfemm('eo_getnode(' + num(n) + ')' );

def eo_getperm(x,y):
	z=eo_getpointvalues(x,y)
	return [z[5],z[6]]

def eo_getpointvalues(x,y):
	z=callfemm('eo_getpointvalues(' + numc(x) + num(y) + ')');
	if len(z)>0 :
		return z
	return [0,0,0,0,0,0,0,0]

def eo_getprobleminfo():
	return callfemm('eo_getprobleminfo()');

def eo_getv(x,y):
	z=eo_getpointvalues(x,y)
	return z[0]

def eo_groupselectblock(*arg):
	callfemm('eo_groupselectblock' + doargs(*arg))

def eo_hidecontourplot():
	callfemm('eo_hidecontourplot()');

def eo_hidedensityplot():
	callfemm('eo_hidedensityplot()');

def eo_hidegrid():
	callfemm('eo_hidegrid()');

def eo_hidemesh():
	callfemm('eo_hidemesh()');

def eo_hidenames():
	callfemm('eo_shownames(0)');

def eo_hidepoints():
	callfemm('eo_hidepoints()');

def eo_lineintegral(ptype):
	return callfemm('eo_lineintegral(' + num(ptype) + ')' );

def eo_makeplot(*arg):
	callfemm('eo_makeplot' + doargs(*arg))

def eo_maximize():
	callfemm('eo_maximize()');

def eo_minimize():
	callfemm('eo_minimize()');

def eo_numelements():
	return callfemm('eo_numelements()');

def eo_numnodes():
	return callfemm('eo_numnodes()');

def eo_refreshview():
	callfemm('eo_refreshview()');

def eo_reload():
	callfemm('eo_reload()');

def eo_resize(nWidth,nHeight):
	callfemm('eo_resize('+ numc(nWidth)+ num(nHeight)+ ')' );

def eo_restore():
	callfemm('eo_restore()');

def eo_savebitmap(fn):
	callfemm('eo_savebitmap(' + quote(fixpath(fn)) + ')' );

def eo_savemetafile(fn):
	callfemm('eo_savemetafile(' + quote(fixpath(fn)) + ')' );

def eo_selectblock(x,y):
	callfemm('eo_selectblock(' + numc(x) + num(y) + ')' )
	
def eo_selectpoint(x,y):
	callfemm('eo_selectpoint(' + numc(x) + num(y) + ')' );

def eo_seteditmode(mode):
	callfemm('eo_seteditmode(' + quote(mode) + ')' );

def eo_setgrid(density,ptype):
	callfemm('eo_setgrid(' + numc(density) + quote(ptype) + ')' );

def eo_showcontourplot(numcontours,al,au):
	callfemm('eo_showcontourplot(' + numc(numcontours) + numc(al) + num(au) + ')' );

def eo_showdensityplot(legend,gscale,ptype,bu,bl):
	callfemm('eo_showdensityplot(' + numc(legend) + numc(gscale) + numc(ptype) + numc(bu) + num(bl) + ')' );

def eo_showgrid():
	callfemm('eo_showgrid()');

def eo_showmesh():
	callfemm('eo_showmesh()');

def eo_shownames():
	callfemm('eo_shownames(1)');

def eo_showpoints():
	callfemm('eo_showpoints()');

def eo_showvectorplot(*arg):
	callfemm('eo_showvectorplot' + doargs(*arg))

def eo_smooth(flag):
	callfemm('eo_smooth(' + quote(flag) + ')' );

def eo_smoothoff():
	callfemm('eo_smooth("off")');

def eo_smoothon():
	callfemm('eo_smooth("on")');

def eo_snapgrid(flag):
	callfemm('eo_gridsnap(' + quote(flag) + ')' );

def eo_snapgridoff():
	callfemm('eo_gridsnap("off")');

def eo_snapgridon():
	callfemm('eo_gridsnap("on")');

def eo_zoom(x1,y1,x2,y2):
	callfemm('eo_zoom(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );

def eo_zoomin():
	callfemm('eo_zoomin()');

def eo_zoomnatural():
	callfemm('eo_zoomnatural()');

def eo_zoomout():
	callfemm('eo_zoomout()');

def hi_addarc(x1,y1,x2,y2,angle,maxseg):
	callfemm('hi_addarc(' + numc(x1) + numc(y1) + numc(x2) + numc(y2) + numc(angle) + num(maxseg) + ')');

def hi_addblocklabel(x,y):
	callfemm('hi_addblocklabel(' + numc(x) + num(y) + ')' );

def hi_addboundprop(*arg):
	callfemm('hi_addboundprop' + doargs(*arg))

def hi_addconductorprop(*arg):
	callfemm('hi_addconductorprop' + doargs(*arg));

def hi_addmaterial(*arg):
	callfemm('hi_addmaterial' + doargs(*arg));

def hi_addnode(x,y):
	callfemm('hi_addnode(' + numc(x) + num(y) + ')');

def hi_addpointprop(*arg):
	callfemm('hi_addpointprop' + doargs(*arg))

def hi_addsegment(x1,y1,x2,y2):
	callfemm('hi_addsegment(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );

def hi_addtkpoint(name,b,h):
	callfemm('hi_addtkpoint(' + quotec(name) + numc(b) + num(h) + ')' );
	
def hi_analyze(*arg):
	callfemm('hi_analyze' + doargs(*arg))

def hi_analyse(n):
	hi_analyze(n)
	
def hi_attachdefault():
	callfemm('hi_attachdefault()');

def hi_attachouterspace():
	callfemm('hi_attachouterspace()');

def hi_clearselected():
	callfemm('hi_clearselected()');

def hi_cleartkpoints(n):
	callfemm('hi_cleartkpoints(' + quote(n) + ')' );

def hi_close():
	callfemm('hi_close()');

def hi_copyrotate(bx,by,angle,copies):
	callfemm('hi_copyrotate(' + numc(bx) + numc(by) + numc(angle) + num(copies) + ')' );

def hi_copyrotate2(bx,by,angle,copies,editaction):
	callfemm('hi_copyrotate(' + numc(bx) + numc(by) + numc(angle) + numc(copies) + num(editaction) + ')' );

def hi_copytranslate(bx,by,copies):
	callfemm('hi_copytranslate(' + numc(bx) + numc(by) + num(copies) + ')' );

def hi_copytranslate2(bx,by,copies,editaction):
	callfemm('hi_copytranslate(' + numc(bx) + numc(by) + numc(copies) + num(editaction) + ')' );

def hi_createmesh():
	return callfemm('hi_createmesh()');

def hi_createradius(x,y,r):
	callfemm('hi_createradius(' + numc(x) + numc(y)+ num(r) + ')' );

def hi_defineouterspace(Zo,Ro,Ri):
	callfemm('hi_defineouterspace(' + numc(Zo) + numc(Ro) + num(Ri) + ')' );

def hi_deleteboundprop(n):
	callfemm('hi_deleteboundprop(' + quote(n) + ')' );

def hi_deleteconductor(n):
	callfemm('hi_deleteconductor(' + quote(n) + ')' );

def hi_deletematerial(n):
	callfemm('hi_deletematerial(' + quote(n) + ')' );

def hi_deletepointprop(n):
	callfemm('hi_deletepointprop(' + quote(n) + ')' );

def hi_deleteselected():
	callfemm('hi_deleteselected()');

def hi_deleteselectedarcsegments():
	callfemm('hi_deleteselectedarcsegments()');

def hi_deleteselectedlabels():
	callfemm('hi_deleteselectedlabels()');

def hi_deleteselectednodes():
	callfemm('hi_deleteselectednodes()');

def hi_deleteselectedsegments():
	callfemm('hi_deleteselectedsegments()');

def hi_detachdefault():
	callfemm('hi_detachdefault()');

def hi_detachouterspace():
	callfemm('hi_detachouterspace()');

def hi_drawarc(x1,y1,x2,y2,angle,maxseg):
	hi_addnode(x1,y1);
	hi_addnode(x2,y2);
	hi_addarc(x1,y1,x2,y2,angle,maxseg);

def hi_drawline(x1,y1,x2,y2):
	hi_addnode(x1,y1);
	hi_addnode(x2,y2);
	hi_addsegment(x1,y1,x2,y2);

def hi_drawrectangle(x1,y1,x2,y2):
	hi_drawline(x1,y1,x2,y1);
	hi_drawline(x2,y1,x2,y2);
	hi_drawline(x2,y2,x1,y2);
	hi_drawline(x1,y2,x1,y1);

def hi_getmaterial(matname):
	callfemm('hi_getmaterial(' + quote(matname) + ')' );

def hi_hidegrid():
	callfemm('hi_hidegrid()');

def hi_hidenames():
	callfemm('hi_shownames(0)');

def hi_loadsolution():
	callfemm('hi_loadsolution()');

def hi_makeABC(*arg):
	callfemm('hi_makeABC' + doargs(*arg))

def hi_maximize():
	callfemm('hi_maximize()');

def hi_minimize():
	callfemm('hi_minimize()');

def hi_mirror(x1,y1,x2,y2):
	callfemm('hi_mirror(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );

def hi_mirror2(x1,y1,x2,y2,editaction):
	callfemm('hi_mirror(' + numc(x1) + numc(y1) + numc(x2) + numc(y2) + num(editaction) + ')' );

def hi_modifyboundprop(*arg):
	callfemm('hi_modifyboundprop' + doargs(*arg))

def hi_modifyconductorprop(*arg):
	callfemm('hi_modifyconductorprop' + doargs(*arg))
	
def hi_modifymaterial(*arg):
	callfemm('hi_modifymaterial' + doargs(*arg))

def hi_modifypointprop(*arg):
	callfemm('hi_modifypointprop' + doargs(*arg))

def hi_moverotate(bx,by,shiftangle):
	callfemm('hi_moverotate(' + numc(bx) + numc(by) + num(shiftangle) + ')' );

def hi_movetranslate(bx,by):
	callfemm('hi_movetranslate(' + numc(bx) + num(by) + ')' );

def hi_movetranslate2(bx,by,editaction):
	callfemm('hi_movetranslate(' + numc(bx) + numc(by) + num(editaction) + ')' );

def hi_probdef(*arg):
	callfemm('hi_probdef' + doargs(*arg))

def hi_purgemesh():
	callfemm('hi_purgemesh()');

def hi_readdxf(docname):
	callfemm('print(hi_readdxf(' + quote(docname) + '))' );

def hi_refreshview():
	callfemm('hi_refreshview()');

def hi_resize(nWidth,nHeight):
	callfemm('hi_resize('+ numc(nWidth)+ num(nHeight)+ ')' );

def hi_restore():
	callfemm('hi_restore()');

def hi_saveas(fn):
	callfemm('hi_saveas(' + quote(fixpath(fn)) + ')');

def hi_savebitmap(n):
	callfemm('hi_savebitmap(' + quote(n) + ')' );

def hi_savedxf(docname):
	callfemm_noeval('hi_savedxf(' + quote(docname) + ')' );

def hi_savemetafile(n):
	callfemm('hi_savemetafile(' + quote(n) + ')' );

def hi_scale(bx,by,sc):
	callfemm('hi_scale(' + numc(bx) + numc(by) + numc(sc) + ')' );

def hi_scale2(bx,by,sc,ea):
	callfemm('hi_scale(' + numc(bx) + numc(by) + numc(sc) + num(ea) + ')' );

def hi_selectarcsegment(x,y):
	return callfemm('hi_selectarcsegment(' + numc(x) + num(y) + ')');

def hi_selectcircle(*arg):
	callfemm('hi_selectcircle' + doargs(*arg));

def hi_selectgroup(gr):
	callfemm('hi_selectgroup(' + num(gr) + ')' );

def hi_selectlabel(x,y):
	return callfemm('hi_selectlabel(' + numc(x) + num(y) + ')');

def hi_selectnode(x,y):
	return callfemm('hi_selectnode(' + numc(x) + num(y) + ')');

def hi_selectrectangle(*arg):
	callfemm('hi_selectrectangle' + doargs(*arg))

def hi_selectsegment(x,y):
	return callfemm('hi_selectsegment(' + numc(x) + num(y) + ')');

def hi_setarcsegmentprop(maxsegdeg,propname,hide,group,incond):
	callfemm('hi_setarcsegmentprop(' + numc(maxsegdeg) + quotec(propname) + numc(hide) + numc(group) + quote(incond) + ')' );

def hi_setblockprop(blockname,automesh,meshsize,group):
	callfemm('hi_setblockprop(' + quotec(blockname) + numc(automesh) + numc(meshsize) + num(group) + ')');

def hi_seteditmode(editmode):
	callfemm('hi_seteditmode(' + quote(editmode) + ')' );

def hi_setfocus(docname):
	callfemm('hi_setfocus(' + quote(docname) + ')' );

def hi_setgrid(density,ptype):
	callfemm('hi_setgrid(' + numc(density) + quote(ptype) + ')' );

def hi_setgroup(n):
	return callfemm('hi_setgroup(' + num(n) + ')' );

def hi_setnodeprop(nodeprop,groupno,inconductor):
	callfemm('hi_setnodeprop(' + quotec(nodeprop) + numc(groupno) + quote(inconductor) + ')');

def hi_setsegmentprop(pn,es,am,hi,gr, inconductor):
	callfemm('hi_setsegmentprop(' + quotec(pn) + numc(es) + numc(am) + numc(hi) + numc(gr) + quote(inconductor) + ')');

def hi_showgrid():
	callfemm('hi_showgrid()');

def hi_showmesh():
	callfemm('hi_showmesh()');

def hi_shownames():
	callfemm('hi_shownames(1)');

def hi_smartmesh(n):
	callfemm('hi_smartmesh(' + num(n)+ ')' );

def hi_snapgridoff():
	callfemm('hi_gridsnap("off")');

def hi_snapgridon():
	callfemm('hi_gridsnap("on")');

def hi_zoom(x1,y1,x2,y2):
	callfemm('hi_zoom(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );

def hi_zoomin():
	callfemm('hi_zoomin()');

def hi_zoomnatural():
	callfemm('hi_zoomnatural()');

def hi_zoomout():
	callfemm('hi_zoomout()');

def hideconsole():
	callfemm('hideconsole()');

def hidepointprops():
	callfemm('hidepointprops()');

def ho_addcontour(x,y):
	callfemm('ho_addcontour(' + numc(x) + num(y) + ')' );

def ho_bendcontour(tta,dtta):
	callfemm('ho_bendcontour(' + numc(tta) + num(dtta) + ')' );

def ho_blockintegral(ptype):
	return callfemm('ho_blockintegral(' + num(ptype) + ')' );
        
def ho_clearblock():
	callfemm('ho_clearblock()');

def ho_clearcontour():
	callfemm('ho_clearcontour()');

def ho_close():
	callfemm('ho_close()');

def ho_getconductorproperties(pname):
	return callfemm('ho_getconductorproperties(' + quote(pname) + ')' );

def ho_getelement(n):
	return callfemm('ho_getelement(' + num(n) + ')' );
	
def ho_getf(x,y):
	z=ho_getpointvalues(x,y);
	return  [z[1],z[2]]

def ho_getg(x,y):
	z=ho_getpointvalues(x,y);
	return  [z[3],z[4]]

def ho_getk(x,y):
	z=ho_getpointvalues(x,y);
	return  [z[5],z[6]]

def ho_getnode(n):
	return callfemm('ho_getnode(' + num(n) + ')' );

def ho_getpointvalues(x,y):
	z=callfemm('ho_getpointvalues(' + numc(x) + num(y) + ')');
	if len(z)>0 :
		return z
	return [0,0,0,0,0,0,0]
	
def ho_getprobleminfo():
	return callfemm('ho_getprobleminfo()');

def ho_gett(x,y):
	z=ho_getpointvalues(x,y);
	return  z[0]

def ho_groupselectblock(*arg):
	callfemm('ho_groupselectblock' + doargs(*arg));

def ho_hidecontourplot():
	callfemm('ho_hidecontourplot()');

def ho_hidedensityplot():
	callfemm('ho_hidedensityplot()');

def ho_hidegrid():
	callfemm('ho_hidegrid()');

def ho_hidemesh():
	callfemm('ho_hidemesh()');

def ho_hidenames():
	callfemm('ho_shownames(0)');

def ho_hidepoints():
	callfemm('ho_hidepoints()');

def ho_lineintegral(ptype):
	return callfemm('ho_lineintegral(' + num(ptype) + ')' );

def ho_makeplot(*arg):
	callfemm('ho_makeplot' + doargs(*arg))

def ho_maximize():
	callfemm('ho_maximize()');

def ho_minimize():
	callfemm('ho_minimize()');

def ho_numelements():
	return callfemm('ho_numelements()');

def ho_numnodes():
	return callfemm('ho_numnodes()');

def ho_refreshview():
	callfemm('ho_refreshview()');

def ho_reload():
	callfemm('ho_reload()');

def ho_resize(nWidth,nHeight):
	callfemm('ho_resize('+ numc(nWidth)+ num(nHeight)+ ')' );

def ho_restore():
	callfemm('ho_restore()');

def ho_savebitmap(fn):
	callfemm('ho_savebitmap(' + quote(fixpath(fn)) + ')' );

def ho_savemetafile(fn):
	callfemm('ho_savemetafile(' + quote(fixpath(fn)) + ')' );

def ho_selectblock(x,y):
	callfemm('ho_selectblock(' + numc(x) + num(y) + ')' );

def ho_selectpoint(x,y):
	callfemm('ho_selectpoint(' + numc(x) + num(y) + ')' );

def ho_seteditmode(mode):
	callfemm('ho_seteditmode(' + quote(mode) + ')' );

def ho_setgrid(density,ptype):
	callfemm('ho_setgrid(' + numc(density) + quote(ptype) + ')' );

def ho_showcontourplot(numcontours,al,au):
	callfemm('ho_showcontourplot(' + numc(numcontours) + numc(al) + num(au) + ')' );

def ho_showdensityplot(legend,gscale,ptype,bu,bl):
	callfemm('ho_showdensityplot(' + numc(legend) + numc(gscale) + numc(ptype) + numc(bu) + num(bl) + ')' );

def ho_showgrid():
	callfemm('ho_showgrid()');

def ho_showmesh():
	callfemm('ho_showmesh()');

def ho_shownames():
	callfemm('ho_shownames(1)');

def ho_showpoints():
	callfemm('ho_showpoints()');

def ho_showvectorplot(*arg):
	callfemm('ho_showvectorplot' + doargs(*arg))
	
def ho_smooth(flag):
	callfemm('ho_smooth(' + quote(flag) + ')' );

def ho_smoothoff():
	callfemm('ho_smooth("off")');

def ho_smoothon():
	callfemm('ho_smooth("on")');

def ho_snapgrid(flag):
	callfemm('ho_gridsnap(' + quote(flag) + ')' );

def ho_snapgridoff():
	callfemm('ho_gridsnap("off")');

def ho_snapgridon():
	callfemm('ho_gridsnap("on")');

def ho_zoom(x1,y1,x2,y2):
	callfemm('ho_zoom(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );

def ho_zoomin():
	callfemm('ho_zoomin()');

def ho_zoomnatural():
	callfemm('ho_zoomnatural()');

def ho_zoomout():
	callfemm('ho_zoomout()');

def IEC(iec):
	return 7.959159641581004*exp(-0.11519673572274754*iec);

def main_maximize():
	callfemm('main_maximize()');

def main_minimize():
	callfemm('main_minimize()');

def main_resize(nWidth,nHeight):
	callfemm('main_resize('+ numc(nWidth)+ num(nHeight)+ ')' );

def messagebox(msg):
	callfemm('messagebox(' + quote(msg) + ')' );

def mi_addarc(x1,y1,x2,y2,angle,maxseg):
	callfemm('mi_addarc(' + numc(x1) + numc(y1) + numc(x2) + numc(y2) + numc(angle) + num(maxseg) + ')');

def mi_addbhpoint(name,b,h):
	callfemm('mi_addbhpoint(' + quotec(name) + numc(b) + num(h) + ')' );

def mi_addblocklabel(x,y):
	callfemm('mi_addblocklabel(' + numc(x) + num(y) + ')' );

def mi_addboundprop(*arg):
	callfemm('mi_addboundprop' + doargs(*arg));

def mi_addcircprop(pname,ic,ptype):
	callfemm('mi_addcircprop(' + quotec(pname) + numc(ic) + num(ptype) + ')' );

def mi_addmaterial(*arg):
	callfemm('mi_addmaterial' + doargs(*arg))

def mi_addnode(x,y):
	callfemm('mi_addnode(' + numc(x) + num(y) + ')');

def mi_addpointprop(pname,ap,jp):
	callfemm('mi_addpointprop(' + quotec(pname) + numc(ap)+ num(jp)+ ')');

def mi_addsegment(x1,y1,x2,y2):
	callfemm('mi_addsegment(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );
	
def mi_analyze(*arg):
	callfemm('mi_analyze' + doargs(*arg));

def mi_analyse(n):
    mi_analyze(n)

def mi_attachdefault():
	callfemm('mi_attachdefault()');

def mi_attachouterspace():
	callfemm('mi_attachouterspace()');

def mi_clearbhpoints(n):
	callfemm('mi_clearbhpoints(' + quote(n) + ')' );

def mi_clearselected():
	callfemm('mi_clearselected()');

def mi_close():
	callfemm('mi_close()');

def mi_copyrotate(bx,by,angle,copies):
	callfemm('mi_copyrotate(' + numc(bx) + numc(by) + numc(angle) + num(copies) + ')' );

def mi_copyrotate2(bx,by,angle,copies,editaction):
	callfemm('mi_copyrotate(' + numc(bx) + numc(by) + numc(angle) + numc(copies) + num(editaction) + ')' );

def mi_copytranslate(bx,by,copies):
	callfemm('mi_copytranslate(' + numc(bx) + numc(by) + num(copies) + ')' );

def mi_copytranslate2(bx,by,copies,editaction):
	callfemm('mi_copytranslate(' + numc(bx) + numc(by) + numc(copies) + num(editaction) + ')' );

def mi_createmesh():
	return callfemm('mi_createmesh()');

def mi_createradius(x,y,r):
	callfemm('mi_createradius(' + numc(x) + numc(y)+ num(r) + ')' );

def mi_defineouterspace(Zo,Ro,Ri):
	callfemm('mi_defineouterspace(' + numc(Zo) + numc(Ro) + num(Ri) + ')' );

def mi_deleteboundprop(n):
	callfemm('mi_deleteboundprop(' + quote(n) + ')' );

def mi_deletecircuit(n):
	callfemm('mi_deletecircuit(' + quote(n) + ')' );

def mi_deletematerial(n):
	callfemm('mi_deletematerial(' + quote(n) + ')' );

def mi_deletepointprop(n):
	callfemm('mi_deletepointprop(' + quote(n) + ')' );

def mi_deleteselected():
	callfemm('mi_deleteselected()');

def mi_deleteselectedarcsegments():
	callfemm('mi_deleteselectedarcsegments()');

def mi_deleteselectedlabels():
	callfemm('mi_deleteselectedlabels()');

def mi_deleteselectednodes():
	callfemm('mi_deleteselectednodes()');

def mi_deleteselectedsegments():
	callfemm('mi_deleteselectedsegments()');

def mi_detachdefault():
	callfemm('mi_detachdefault()');

def mi_detachouterspace():
	callfemm('mi_detachouterspace()');

def mi_drawarc(x1,y1,x2,y2,angle,maxseg):
	mi_addnode(x1,y1)
	mi_addnode(x2,y2)
	mi_addarc(x1,y1,x2,y2,angle,maxseg)

def mi_drawline(x1,y1,x2,y2):
	mi_addnode(x1,y1);
	mi_addnode(x2,y2);
	mi_addsegment(x1,y1,x2,y2);

def mi_drawrectangle(x1,y1,x2,y2):
	mi_drawline(x1,y1,x2,y1);
	mi_drawline(x2,y1,x2,y2);
	mi_drawline(x2,y2,x1,y2);
	mi_drawline(x1,y2,x1,y1);

def mi_getmaterial(matname):
	callfemm('mi_getmaterial(' + quote(matname) + ')' );

def mi_hidegrid():
	callfemm('mi_hidegrid()');

def mi_hidenames():
	callfemm('mi_shownames(0)');

def mi_loadsolution():
	callfemm('mi_loadsolution()');

def mi_makeABC(*arg):
	callfemm('mi_makeABC' + doargs(*arg));

def mi_maximize():
	callfemm('mi_maximize()');

def mi_minimize():
	callfemm('mi_minimize()');

def mi_mirror(x1,y1,x2,y2):
	callfemm('mi_mirror(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );

def mi_mirror2(x1,y1,x2,y2,editaction):
	callfemm('mi_mirror(' + numc(x1) + numc(y1) + numc(x2) + numc(y2) + num(editaction) + ')' );

def mi_modifyboundprop(*arg):
  	callfemm('mi_modifyboundprop' + doargs(*arg));

def mi_modifycircprop(*arg):
    callfemm('mi_modifycircprop' + doargs(*arg));

def mi_modifymaterial(*arg):
	callfemm('mi_modifymaterial' + doargs(*arg));

def mi_modifypointprop(*arg):
	callfemm('mi_modifypointprop' + doargs(*arg));

def mi_moverotate(bx,by,shiftangle):
	callfemm('mi_moverotate(' + numc(bx) + numc(by) + num(shiftangle) + ')' );

def mi_movetranslate(bx,by):
	callfemm('mi_movetranslate(' + numc(bx) + num(by) + ')' );

def mi_movetranslate2(bx,by,editaction):
	callfemm('mi_movetranslate(' + numc(bx) + numc(by) + num(editaction) + ')' );

def mi_probdef(*arg):
	callfemm('mi_probdef' + doargs(*arg));

def mi_purgemesh():
	callfemm('mi_purgemesh()');

def mi_readdxf(docname):
	callfemm('print(mi_readdxf(' + quote(docname) + '))' );

def mi_refreshview():
	callfemm('mi_refreshview()');

def mi_resize(nWidth,nHeight):
	callfemm('mi_resize('+ numc(nWidth)+ num(nHeight)+ ')' );

def mi_restore():
	callfemm('mi_restore()');

def mi_saveas(fn):
	callfemm('mi_saveas(' + quote(fixpath(fn)) + ')' );

def mi_savebitmap(n):
	callfemm('mi_savebitmap(' + quote(n) + ')' );

def mi_savedxf(docname):
	callfemm_noeval('mi_savedxf(' + quote(docname) + ')' );

def mi_savemetafile(n):
	callfemm('mi_savemetafile(' + quote(n) + ')' );

def mi_scale(bx,by,sc):
	callfemm('mi_scale(' + numc(bx) + numc(by) + numc(sc) + ')' );

def mi_scale2(bx,by,sc,ea):
	callfemm('mi_scale(' + numc(bx) + numc(by) + numc(sc) + num(ea) + ')' );

def mi_selectarcsegment(x,y):
	return callfemm('mi_selectarcsegment(' + numc(x) + num(y) + ')');

def mi_selectcircle(*arg):
	callfemm('mi_selectcircle' + doargs(*arg));

def mi_selectgroup(gr):
	callfemm('mi_selectgroup(' + num(gr) + ')' );

def mi_selectlabel(x,y):
	return callfemm('mi_selectlabel(' + numc(x) + num(y) + ')');

def mi_selectnode(x,y): 
	return callfemm('mi_selectnode(' + numc(x) + num(y) + ')');

def mi_selectrectangle(*arg):
	callfemm('mi_selectrectangle' + doargs(*arg));

def mi_selectsegment(x,y):
	return callfemm('mi_selectsegment(' + numc(x) + num(y) + ')');

def mi_setarcsegmentprop(maxsegdeg,propname,hide,group):
	callfemm('mi_setarcsegmentprop(' + numc(maxsegdeg) + quotec(propname) + numc(hide) + num(group) + ')' );

def mi_setblockprop(*arg):
	callfemm('mi_setblockprop' + doargs(*arg));

def mi_setcurrent(name,x):
	mi_modifycircprop(name,1,x);

def mi_seteditmode(editmode):
	callfemm('mi_seteditmode(' + quote(editmode) + ')' );

def mi_setfocus(docname):
	callfemm('mi_setfocus(' + quote(docname) + ')' );

def mi_setgrid(density,ptype):
	callfemm('mi_setgrid(' + numc(density) + quote(ptype) + ')' );

def mi_setgroup(n):
	return callfemm('mi_setgroup(' + num(n) + ')' );

def mi_setnodeprop(nodeprop,groupno):
	callfemm('mi_setnodeprop(' + quotec(nodeprop) + num(groupno) + ')');

def mi_setprevious(*arg):
	callfemm('mi_setprevious' + doargs(*arg));

def mi_setsegmentprop(pn,es,am,hi,gr):
	callfemm('mi_setsegmentprop(' + quotec(pn) + numc(es) + numc(am) + numc(hi) + num(gr) + ')');

def mi_showgrid():
	callfemm('mi_showgrid()');

def mi_showmesh():
	callfemm('mi_showmesh()');

def mi_shownames():
	callfemm('mi_shownames(1)');

def mi_smartmesh(n):
	callfemm('mi_smartmesh(' + num(n)+ ')' );

def mi_snapgridoff():
	callfemm('mi_gridsnap("off")');

def mi_snapgridon():
	callfemm('mi_gridsnap("on")');

def mi_zoom(x1,y1,x2,y2):
	callfemm('mi_zoom(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );

def mi_zoomin():
	callfemm('mi_zoomin()');

def mi_zoomnatural():
	callfemm('mi_zoomnatural()');

def mi_zoomout():
	callfemm('mi_zoomout()');

def mo_addcontour(x,y):
	callfemm('mo_addcontour(' + numc(x) + num(y) + ')' );

def mo_bendcontour(tta,dtta):
	callfemm('mo_bendcontour(' + numc(tta) + num(dtta) + ')' );

def mo_blockintegral(ptype):
	return callfemm('mo_blockintegral(' + num(ptype) + ')' );

def mo_clearblock():
	callfemm('mo_clearblock()');

def mo_clearcontour():
	callfemm('mo_clearcontour()');

def mo_close():
	callfemm('mo_close()');

def mo_gapintegral(bdryname,inttype):
	return callfemm('mo_gapintegral(' + quotec(bdryname) + num(inttype) + ')');

def mo_geta(x,y):
	z=mo_getpointvalues(x,y)
	return z[0]

def mo_getb(x,y):
	z=mo_getpointvalues(x,y);
	return [z[1],z[2]]

def mo_getcircuitproperties(name):
	return callfemm('mo_getcircuitproperties(' + quote(name) + ')' );

def mo_getconductivity(x,y):
	z= mo_getpointvalues(x,y)
	return z[3]

def mo_getelement(n):
	return callfemm('mo_getelement(' + num(n) + ')' );

def mo_getenergydensity(x,y):
	z=mo_getpointvalues(x,y)
	return z[4]

def mo_getfill(x,y):
	z=mo_getpointvalues(x,y);
	return z[13]

def mo_getgapa(bdryname,angle):
	return callfemm('mo_getgapa(' + quotec(bdryname) + num(angle) + ')');

def mo_getgapb(bdryname,angle):
	return callfemm('mo_getgapb(' + quotec(bdryname) + num(angle) + ')');

def mo_getgapharmonics(*arg):
	return callfemm('mo_getgapharmonics' + doargs(*arg))

def mo_geth(x,y):
	z=mo_getpointvalues(x,y)
	return [z[5],z[6]]

def mo_getj(x,y):
	z=mo_getpointvalues(x,y)
	return z[7]+z[8]
	
def mo_getmu(x,y):
	z=mo_getpointvalues(x,y)
	return [z[9],z[10]]

def mo_getnode(n):
	return callfemm('mo_getnode(' + num(n) + ')' );

def mo_getpe(x,y):
	z=mo_getpointvalues(x,y)
	return z[11]
	
def mo_getph(x,y):
	z=mo_getpointvalues(x,y)
	return z[12]

def mo_getpointvalues(x,y):
	z=callfemm('mo_getpointvalues(' + numc(x) + num(y) + ')');
	if len(z)>0 :
		return z
	return [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def mo_getprobleminfo():
	return callfemm('mo_getprobleminfo()');

def mo_groupselectblock(*arg):
	callfemm('mo_groupselectblock' + doargs(*arg))

def mo_hidecontourplot():
	callfemm('mo_hidecontourplot()');

def mo_hidedensityplot():
	callfemm('mo_hidedensityplot()');

def mo_hidegrid():
	callfemm('mo_hidegrid()');

def mo_hidemesh():
	callfemm('mo_hidemesh()');

def mo_hidenames():
	callfemm('mo_shownames(0)');

def mo_hidepoints():
	callfemm('mo_hidepoints()');

def mo_lineintegral(ptype):
	return callfemm('mo_lineintegral(' + num(ptype) + ')');

def mo_makeplot(*arg):
	callfemm('mo_makeplot' + doargs(*arg))

def mo_maximize():
	callfemm('mo_maximize()');

def mo_minimize():
	callfemm('mo_minimize()');

def mo_numelements():
	return callfemm('mo_numelements()');

def mo_numnodes():
	return callfemm('mo_numnodes()');

def mo_refreshview():
	callfemm('mo_refreshview()');

def mo_reload():
	callfemm('mo_reload()');

def mo_resize(nWidth,nHeight):
	callfemm('mo_resize('+ numc(nWidth)+ num(nHeight)+ ')' );

def mo_restore():
	callfemm('mo_restore()');

def mo_savebitmap(fn):
	callfemm('mo_savebitmap(' + quote(fixpath(fn)) + ')' );

def mo_savemetafile(fn):
	callfemm('mo_savemetafile(' + quote(fixpath(fn)) + ')' );

def mo_selectblock(x,y):
	callfemm('mo_selectblock(' + numc(x) + num(y) + ')' );

def mo_selectpoint(x,y):
	callfemm('mo_selectpoint(' + numc(x) + num(y) + ')' );

def mo_seteditmode(mode):
	callfemm('mo_seteditmode(' + quote(mode) + ')' );

def mo_setgrid(density,ptype):
	callfemm('mo_setgrid(' + numc(density) + quote(ptype) + ')' );

def mo_setweightingscheme(n):
	callfemm('mo_setweightingscheme(' + num(n) + ')' );

def mo_showcontourplot(numcontours,al,au,ptype):
	callfemm('mo_showcontourplot(' + numc(numcontours) + numc(al) + numc(au) + quote(ptype) + ')' );

def mo_showdensityplot(legend,gscale,bu,bl,ptype):
	callfemm('mo_showdensityplot(' + numc(legend) + numc(gscale) + numc(bu) + numc(bl) + quote(ptype) + ')' );

def mo_showgrid():
	callfemm('mo_showgrid()');

def mo_showmesh():
	callfemm('mo_showmesh()');

def mo_shownames():
	callfemm('mo_shownames(1)');

def mo_showpoints():
	callfemm('mo_showpoints()');

def mo_showvectorplot(*arg):
	callfemm('mo_showvectorplot' + doargs(*arg))

def mo_smooth(flag):
	callfemm('mo_smooth(' + quote(flag) + ')' );

def mo_smoothoff():
	callfemm('mo_smooth("off")');

def mo_smoothon():
	callfemm('mo_smooth("on")');

def mo_snapgrid(flag):
	callfemm('mo_gridsnap(' + quote(flag) + ')' );

def mo_snapgridoff():
	callfemm('mo_gridsnap("off")');

def mo_snapgridon():
	callfemm('mo_gridsnap("on")');

def mo_zoom(x1,y1,x2,y2):
	callfemm('mo_zoom(' + numc(x1) + numc(y1) + numc(x2) + num(y2) + ')' );

def mo_zoomin():
	callfemm('mo_zoomin()');

def mo_zoomnatural():
	callfemm('mo_zoomnatural()');

def mo_zoomout():
	callfemm('mo_zoomout()');

def opendocument(fn):
	callfemm( 'open(' + quote(fixpath(fn)) + ')' );

def prompt(msg):
	return callfemm('prompt(' + quote(msg) + ')' );
        
def showconsole():
	callfemm('showconsole()');

def showpointprops():
	callfemm('showpointprops()');

def smartmesh(n):
	callfemm('smartmesh(' + num(n)+ ')' );

