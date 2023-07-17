El archivo csv para cargar las personas tiene que tener este encabezado
    num_orden,dni,apellido,nombre,clase,domicilio,mesa

Para weasyprint, instalar las siguientes dependencias de acuerdo al sistema operativo
    En linux:
        apt-get install python3-dev python3-pip python3-setuptools python3-wheel libffi-dev libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
        apt-get install libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev libffi-dev shared-mime-info

    En mac:
        brew install python3 cairo pango gdk-pixbuf libffi

    En windows:
        Instalar GTK3 https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
        Crear entorno virtual una vez instalado
