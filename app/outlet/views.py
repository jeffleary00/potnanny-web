from flask import render_template, redirect, request, session
from flask import jsonify
from flask_login import login_required
from app import app, db
from .models import Outlet
from .forms import OutletForm


@app.route('/outlet')
@login_required
def outlet_index():
    outlets = Outlet.query.all()
    return render_template('outlet/index.html', 
                title='Outlets',
                payload=outlets)


@app.route('/outlet/create', methods=['GET','POST'])
@app.route('/outlet/<pk>/edit', methods=['GET','POST'])
@login_required
def outlet_edit(pk=None):
    obj = None
    title = 'Add Outlet'

    if pk:
        title = 'Edit Outlet'
        obj = Outlet.query.get_or_404(int(pk))
        
    form = OutletForm(obj=obj)  
    if request.method == 'POST' and form.validate_on_submit():
        if pk:
            form.populate_obj(obj)
        else:
            o = Outlet(form.name.data, int(form.channel.data))
            db.session.add(o)
    
        db.session.commit()
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        else:
            return redirect('/outlet')

    return render_template('outlet/form.html', 
        form=form,
        title=title,
        pk=pk)    


@app.route('/outlet/<pk>/delete', methods=['POST'])
@login_required
def outlet_delete(pk):
    o = Outlet.query.get_or_404(int(pk))
    db.session.delete(o)
    db.session.commit()
    if request.args.get("next"):
        return redirect(request.args.get("next"))
    else:
        return redirect('/outlet')
    

@app.route('/outlet/<pk>/toggle', methods=['POST'])
@login_required
def outlet_toggle(pk):
    o = Outlet.query.get_or_404(int(pk))

    if o.state == 1 or o.state is True:
        rval = o.off()
    else:
        rval = o.on()

    if not rval:
        db.session.commit()

    return jsonify(o.simplified())


@app.route('/outlet/<pk>', methods=['GET'])
def outlet_status(pk):
    o = Outlet.query.get_or_404(int(pk))
    return jsonify(o.simplified())


