#include "system_speed.h"

STATIC MP_DEFINE_CONST_FUN_OBJ_1(system_speed_set_obj, system_speed_set);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(system_speed_vbus_get_obj, system_speed_vbus_get);

STATIC const mp_map_elem_t system_speed_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_system_speed) },
    { MP_ROM_QSTR(MP_QSTR_set_speed), MP_ROM_PTR(&system_speed_set_obj) },
    { MP_ROM_QSTR(MP_QSTR_get_vbus), MP_ROM_PTR(&system_speed_vbus_get_obj) },

    { MP_ROM_QSTR(MP_QSTR_SYSTEM_VERY_SLOW), MP_ROM_INT(0) },
    { MP_ROM_QSTR(MP_QSTR_SYSTEM_SLOW), MP_ROM_INT(1) },
    { MP_ROM_QSTR(MP_QSTR_SYSTEM_NORMAL), MP_ROM_INT(2) },
    { MP_ROM_QSTR(MP_QSTR_SYSTEM_FAST), MP_ROM_INT(3) },
    { MP_ROM_QSTR(MP_QSTR_SYSTEM_TURBO), MP_ROM_INT(4) },
};
STATIC MP_DEFINE_CONST_DICT(mp_module_system_speed_globals, system_speed_globals_table);

const mp_obj_module_t system_speed_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&mp_module_system_speed_globals,
};

#if MICROPY_VERSION <= 70144
MP_REGISTER_MODULE(MP_QSTR_system_speed, system_speed_user_cmodule, MODULE_SYSTEM_SPEED_ENABLED);
#else
MP_REGISTER_MODULE(MP_QSTR_system_speed, system_speed_user_cmodule);
#endif