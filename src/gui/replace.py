import pygtk
import gtk

def replace_widget(current, new):
    """
    Replace one widget with another.
    'current' has to be inside a container (e.g. gtk.VBox).
    """
    container = current.parent
    assert container # is "current" inside a container widget?

    # stolen from gazpacho code (widgets/base/base.py):
    props = {}
    for pspec in gtk.container_class_list_child_properties(container):
        props[pspec.name] = container.child_get_property(current, pspec.name)

    gtk.Container.remove(container, current)
    container.add(new)

    for name, value in props.items():
        container.child_set_property(new, name, value)

def destroy(widget, data=None):
    gtk.main_quit()

def wrap_in_button(label):
    text = label.get_text()
    button = gtk.Button(text)

    replace_widget(label, button)

def Main():
    # Pretend that this chunk is actually replaced by GTKBuilder work
    # From here...
    window = gtk.Window()
    window.connect('destroy', destroy)

    box = gtk.VBox()
    window.add(box)

    label1 = gtk.Label("Label 1")
    label2 = gtk.Label("Label 2")
    label3 = gtk.Label("Label 3")

    box.pack_start(label1)
    box.pack_start(label2)
    box.pack_start(label3)

    # ...up to here

    #wrap_in_button(label2)

    window.show_all()
    gtk.main()

if __name__ == "__main__":
    Main()