# This module contains cortex-m bsp support
from support.bsp_sources.archsupport import ArchSupport
from support.bsp_sources.target import Target

import glob


class CortexMArch(ArchSupport):
    @property
    def name(self):
        return "cortex-m"

    def __init__(self):
        super(CortexMArch, self).__init__()
        self.add_sources('arch', [
            'src/s-macres__cortexm3.adb',
            'arm/src/breakpoint_handler-cortexm.S'])
        self.add_sources('gnarl', [
            'src/s-bbcpsp__cortexm.ads',
            'src/s-bbcppr__old.ads',
            'src/s-bbcppr__armv7m.adb',
            'src/s-bbinte__generic.adb',
            'src/s-bbsumu__generic.adb',
            'src/s-bcpcst__armvXm.ads'])


class ArmV7MArch(ArchSupport):
    @property
    def name(self):
        return "armv7-m"

    @property
    def parent(self):
        return CortexMArch

    def __init__(self):
        super(ArmV7MArch, self).__init__()
        self.add_sources('gnarl', [
            'src/s-bbbosu__armv7m.adb',
            'src/s-bcpcst__pendsv.adb'])


class ArmV6MTarget(Target):
    @property
    def target(self):
        return "arm-eabi"

    @property
    def parent(self):
        return CortexMArch

    @property
    def has_timer_64(self):
        return False

    @property
    def has_single_precision_fpu(self):
        return False

    @property
    def has_double_precision_fpu(self):
        return False

    @property
    def has_small_memory(self):
        return True

    def __init__(self):
        super(ArmV6MTarget, self).__init__()


class ArmV7MTarget(ArmV6MTarget):
    @property
    def parent(self):
        return ArmV7MArch

    @property
    def has_single_precision_fpu(self):
        return True

    @property
    def system_ads(self):
        return {'zfp': 'system-xi-arm.ads',
                'ravenscar-sfp': 'system-xi-cortexm4-sfp.ads',
                'ravenscar-full': 'system-xi-cortexm4-full.ads'}

    def __init__(self):
        super(ArmV7MTarget, self).__init__()


class LM3S(ArmV7MTarget):
    @property
    def name(self):
        return 'lm3s'

    @property
    def loaders(self):
        return ('ROM', 'RAM', 'USER')

    @property
    def has_single_precision_fpu(self):
        return False

    @property
    def has_fpu(self):
        # Still add floating point attributes
        return True

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mthumb', '-msoft-float',
                '-mcpu=cortex-m3')

    @property
    def readme_file(self):
        return 'arm/lm3s/README'

    @property
    def system_ads(self):
        # Only zfp supported here
        ret = super(LM3S, self).system_ads
        return {'zfp': ret['zfp']}

    def __init__(self):
        super(LM3S, self).__init__()

        self.add_linker_script('arm/lm3s/lm3s-rom.ld', 'ROM')
        self.add_linker_script('arm/lm3s/lm3s-ram.ld', 'RAM')
        self.add_sources('crt0', [
            'arm/lm3s/start-rom.S',
            'arm/lm3s/start-ram.S',
            'arm/lm3s/setup_pll.adb',
            'arm/lm3s/setup_pll.ads',
            'src/s-textio__lm3s.adb'])


class SamCommonArchSupport(ArchSupport):
    @property
    def name(self):
        return 'sam'

    @property
    def parent(self):
        return ArmV7MArch

    @property
    def loaders(self):
        return ('ROM', 'SAMBA', 'USER')

    def __init__(self):
        super(SamCommonArchSupport, self).__init__()

        self.add_linker_script('arm/sam/common-SAMBA.ld', loader='SAMBA')
        self.add_linker_script('arm/sam/common-ROM.ld', loader='ROM')

        self.add_sources('crt0', [
            'arm/sam/start-rom.S',
            'arm/sam/start-ram.S',
            'arm/sam/setup_pll.ads'])
        self.add_sources('gnarl', [
            'src/s-bbpara__sam4s.ads'])


class Sam(ArmV7MTarget):
    @property
    def name(self):
        return self.board

    @property
    def parent(self):
        return SamCommonArchSupport

    @property
    def has_single_precision_fpu(self):
        if self.board == 'sam4s' or self.board == 'sam3x8e':
            return False
        else:
            return True

    @property
    def system_ads(self):
        # No runtime full -- WHY NOT?
        return super(Sam, self).system_ads
        # return {'zfp': ret['zfp'],
                # 'ravenscar-sfp': ret['ravenscar-sfp']}

    @property
    def compiler_switches(self):
        switches = ('-mlittle-endian', '-mthumb')
        if self.has_single_precision_fpu:
            switches += ('-mhard-float', '-mfpu=fpv4-sp-d16')
        else:
            switches += ('-msoft-float', ) # single element tuple
        
        if self.name == 'sam3x8e':
            switches += ('-mcpu=cortex-m3', )
        else:
            switches += ('-mcpu=cortex-m4', )
        return switches

    def __init__(self, board):
        assert board in ('sam4s', 'samg55', 'sam3x8e'), "Unexpected SAM board %s" % board
        self.board = board
        super(Sam, self).__init__()

        self.add_linker_script(
            'arm/sam/%s/memory-map.ld' % self.name,
            loader=('SAMBA', 'ROM'))
            
        if board == 'sam3x8e':
            self.add_sources('crt0', [
                'arm/sam/s-sam3x8.ads',
                'src/s-textio__sam3x8e.adb',
                glob.glob('arm/sam/sam3x8e/svd/i-sam3x8e*.ads')]) # add all BSP sources
        else:
            self.add_sources('crt0', [
                'arm/sam/s-sam4s.ads',
                'src/s-textio__sam4s.adb',
                'arm/sam/%s/svd/i-%s.ads' % (self.name, self.name),
                'arm/sam/%s/svd/i-%s-efc.ads' % (self.name, self.name),
                'arm/sam/%s/svd/i-%s-pmc.ads' % (self.name, self.name),
                'arm/sam/%s/svd/i-%s-sysc.ads' % (self.name, self.name)])
            
        self.add_sources('crt0', [
            'arm/sam/%s/board_config.ads' % self.name,
            'arm/sam/%s/setup_pll.adb' % self.name])
        # FIXME: s-textio.adb is invalid for the g55

        # ravenscar support
        self.add_sources('gnarl', [
            'arm/sam/%s/svd/handler.S' % self.name,
            'arm/sam/%s/s-bbbopa.ads' % self.name,
            'arm/sam/%s/s-bbmcpa.ads' % self.name,
            'arm/sam/%s/svd/a-intnam.ads' % self.name])


class SmartFusion2(ArmV7MTarget):
    @property
    def name(self):
        return 'smartfusion2'

    @property
    def loaders(self):
        return ('ROM', 'USER')

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mthumb', '-msoft-float',
                '-mcpu=cortex-m3')

    @property
    def has_single_precision_fpu(self):
        return False

    @property
    def has_fpu(self):
        # Still add floating point attributes
        return True

    @property
    def system_ads(self):
        # no zfp nor ravenscar-full rts
        ret = super(SmartFusion2, self).system_ads
        return {'ravenscar-sfp': ret['ravenscar-sfp']}

    def __init__(self):
        super(SmartFusion2, self).__init__()

        self.add_linker_script('arm/smartfusion2/common-ROM.ld', loader='ROM')
        self.add_linker_script('arm/smartfusion2/memory-map.ld', loader='ROM')

        self.add_sources('crt0', [
            'arm/smartfusion2/start-rom.S',
            'arm/smartfusion2/setup_pll.adb',
            'arm/smartfusion2/setup_pll.ads',
            'arm/smartfusion2/s-sf2.ads',
            'arm/smartfusion2/s-sf2.adb',
            'arm/smartfusion2/s-sf2uar.ads',
            'arm/smartfusion2/s-sf2uar.adb',
            'arm/smartfusion2/svd/i-sf2.ads',
            'arm/smartfusion2/svd/i-sf2-system_registers.ads',
            'arm/smartfusion2/svd/i-sf2-mmuart.ads',
            'arm/smartfusion2/svd/i-sf2-gpio.ads',
            'arm/smartfusion2/s-textio.adb'])
        self.add_sources('gnarl', [
            'arm/smartfusion2/s-sf2gpi.ads',
            'arm/smartfusion2/s-sf2gpi.adb',
            'arm/smartfusion2/svd/handler.S',
            'arm/smartfusion2/svd/a-intnam.ads',
            'src/s-bbpara__smartfusion2.ads'])


class M1AGL(ArmV6MTarget):
    @property
    def name(self):
        return 'm1agl'

    @property
    def loaders(self):
        return (['ROM', 'RAM'])

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mthumb', '-msoft-float',
                '-mcpu=cortex-m1')

    @property
    def system_ads(self):
        return {'zfp': 'system-xi-arm.ads',
                'ravenscar-sfp': 'system-xi-m1agl-sfp.ads'}

    def __init__(self):
        super(M1AGL, self).__init__()

        self.add_linker_script('arm/igloo/m1agl/common-ROM.ld', loader='ROM')
        self.add_linker_script('arm/igloo/m1agl/common-RAM.ld', loader='RAM')
        self.add_linker_script('arm/igloo/m1agl/memory-map.ld',
                               loader=['ROM', 'RAM'])

        self.add_sources('crt0', [
            'arm/igloo/m1agl/start-rom.S',
            'arm/igloo/m1agl/start-ram.S',
            'arm/igloo/m1agl/s-bbbopa.ads',
            'arm/igloo/m1agl/s-bbmcpa.ads',
            'arm/igloo/m1agl/s-textio.adb',
            'arm/src/armv6m_irq_trap_without_os_extensions.S'])

        self.add_sources('gnarl', [
            'arm/igloo/m1agl/a-intnam.ads',
            'arm/igloo/m1agl/svd/i-m1agl.ads',
            'arm/igloo/m1agl/svd/i-m1agl-coretimer.ads',
            'arm/igloo/m1agl/svd/i-m1agl-coreinterrupt.ads',
            'arm/igloo/m1agl/svd/i-m1agl-coreuartapb.ads',
            'src/s-bbpara__m1agl.ads',
            'src/s-bbbosu__m1agl.adb',
            'src/s-bcpcst__m1agl.adb'])


class NRF51(ArmV6MTarget):
    @property
    def name(self):
        return 'nRF51'

    @property
    def loaders(self):
        return (['ROM'])

    @property
    def has_fpu(self):
        return True

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mthumb', '-msoft-float',
                '-mcpu=cortex-m0')

    @property
    def system_ads(self):
        return {'zfp': 'system-xi-arm.ads',
                'ravenscar-sfp': 'system-xi-armv6m-sfp.ads',
                'ravenscar-full': 'system-xi-armv6m-full.ads'}

    def __init__(self):
        super(NRF51, self).__init__()

        self.add_linker_script('arm/nordic/nrf51/common-ROM.ld', loader='ROM')

        self.add_sources('crt0', [
            'src/s-bbarat.ads',
            'src/s-bbarat.adb',
            'arm/nordic/nrf51/svd/i-nrf51.ads',
            'arm/nordic/nrf51/svd/i-nrf51-clock.ads',
            'arm/nordic/nrf51/svd/i-nrf51-rtc.ads',
            'arm/nordic/nrf51/svd/i-nrf51-uart.ads',
            'arm/nordic/nrf51/svd/handler.S',
            'arm/nordic/nrf51/start-rom.S',
            'arm/nordic/nrf51/s-bbmcpa.ads'])

        self.add_sources('gnarl', [
            'arm/nordic/nrf51/svd/a-intnam.ads',
            'src/s-bbpara__nrf51.ads',
            'src/s-bbbosu__nrf51.adb',
            'src/s-bcpcst__pendsv.adb'])


class Microbit(NRF51):
    @property
    def name(self):
        return 'microbit'

    @property
    def use_semihosting_io(self):
        return False

    def __init__(self):
        super(Microbit, self).__init__()

        self.add_linker_script('arm/nordic/nrf51/memory-map_nRF51822xxAA.ld',
                               loader='ROM')

        self.add_sources('crt0',
                         ['arm/nordic/nrf51/s-bbbopa__microbit.ads',
                          'src/s-textio__microbit.adb'])


class Stm32CommonArchSupport(ArchSupport):
    """Holds sources common to all stm32 boards"""
    @property
    def name(self):
        return 'stm32'

    @property
    def parent(self):
        return ArmV7MArch

    @property
    def loaders(self):
        return ('ROM', 'RAM', 'USER')

    @property
    def readme_file(self):
        return 'arm/stm32/README'

    def __init__(self):
        super(Stm32CommonArchSupport, self).__init__()

        self.add_linker_script('arm/stm32/common-RAM.ld', loader='RAM')
        self.add_linker_script('arm/stm32/common-ROM.ld', loader='ROM')

        self.add_sources('crt0', [
            'src/s-bbpara__stm32f4.ads',
            'arm/stm32/s-stm32.ads',
            'arm/stm32/start-rom.S',
            'arm/stm32/start-ram.S',
            'arm/stm32/start-common.S',
            'arm/stm32/setup_pll.adb',
            'arm/stm32/setup_pll.ads'])


class Stm32(ArmV7MTarget):
    """Generic handling of stm32 boards"""
    @property
    def name(self):
        return self.board

    @property
    def parent(self):
        return Stm32CommonArchSupport

    @property
    def use_semihosting_io(self):
        return True

    @property
    def has_double_precision_fpu(self):
        if self.mcu == 'stm32f7x9':
            return True
        else:
            return False

    @property
    def cortex(self):
        if self.mcu.startswith('stm32f4'):
            return 'cortex-m4'
        elif self.mcu.startswith('stm32f7'):
            return 'cortex-m7'
        else:
            assert False, "Unexpected MCU %s" % self.mcu

    @property
    def fpu(self):
        if self.cortex == 'cortex-m4':
            return 'fpv4-sp-d16'
        elif not self.has_double_precision_fpu:
            return 'fpv5-sp-d16'
        else:
            return 'fpv5-d16'

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mhard-float',
                '-mcpu=%s' % self.cortex,
                '-mfpu=%s' % self.fpu,
                '-mthumb')

    def __init__(self, board):
        self.board = board
        if self.board == 'stm32f4':
            self.mcu = 'stm32f40x'
        elif self.board == 'stm32f429disco':
            self.mcu = 'stm32f429x'
        elif self.board == 'openmv2':
            self.mcu = 'stm32f429x'
        elif self.board == 'stm32f469disco':
            self.mcu = 'stm32f469x'
        elif self.board == 'stm32f746disco':
            self.mcu = 'stm32f7x'
        elif self.board == 'stm32756geval':
            self.mcu = 'stm32f7x'
        elif self.board == 'stm32f769disco':
            self.mcu = 'stm32f7x9'
        else:
            assert False, "Unknown stm32 board: %s" % self.board

        super(Stm32, self).__init__()

        self.add_linker_script('arm/stm32/%s/memory-map.ld' % self.mcu,
                               loader=('RAM', 'ROM'))
        # startup code
        self.add_sources('crt0', [
            'arm/stm32/%s/s-bbbopa.ads' % self.mcu,
            'arm/stm32/%s/s-bbmcpa.ads' % self.mcu,
            'arm/stm32/%s/s-bbmcpa.adb' % self.mcu,
            'arm/stm32/%s/svd/i-stm32.ads' % self.mcu,
            'arm/stm32/%s/svd/i-stm32-flash.ads' % self.mcu,
            'arm/stm32/%s/svd/i-stm32-gpio.ads' % self.mcu,
            'arm/stm32/%s/svd/i-stm32-pwr.ads' % self.mcu,
            'arm/stm32/%s/svd/i-stm32-rcc.ads' % self.mcu,
            'arm/stm32/%s/svd/i-stm32-syscfg.ads' % self.mcu,
            'arm/stm32/%s/svd/i-stm32-usart.ads' % self.mcu])

        if self.board == 'stm32f4':
            self.add_sources('crt0', [
                'arm/stm32/stm32f40x/s-stm32.adb'])
        elif self.board == 'stm32f429disco':
            self.add_sources('crt0', [
                'arm/stm32/stm32f429x/s-stm32.adb'])
        elif self.board == 'openmv2':
            self.add_sources('crt0', [
                'arm/stm32/stm32f429x/s-stm32.adb'])
            self.update_pair(
                's-bbbopa.ads', 'arm/stm32/%s/s-bbbopa-openmv2.ads' % self.mcu)
        elif self.board == 'stm32f469disco':
            self.add_sources('crt0', [
                'arm/stm32/stm32f429x/s-stm32.adb'])
        elif self.board == 'stm32f746disco':
            self.add_sources('crt0', [
                'arm/stm32/stm32f7x/s-stm32.adb'])
        elif self.board == 'stm32756geval':
            self.add_sources('crt0', [
                'arm/stm32/stm32f7x/s-stm32.adb'])
            self.update_pair(
                's-bbbopa.ads',
                'arm/stm32/%s/s-bbbopa-stm32756geval.ads' % self.mcu)
        elif self.board == 'stm32f769disco':
            self.add_sources('crt0', [
                'arm/stm32/stm32f7x/s-stm32.adb'])

        # ravenscar support
        self.add_sources('gnarl', [
            'arm/stm32/%s/svd/handler.S' % self.mcu,
            'arm/stm32/%s/svd/a-intnam.ads' % self.mcu])


class CortexM0(ArmV6MTarget):
    @property
    def name(self):
        return 'cortex-m0'

    @property
    def has_fpu(self):
        return True

    @property
    def use_semihosting_io(self):
        return True

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mthumb', '-msoft-float',
                '-mcpu=cortex-m0')

    @property
    def system_ads(self):
        return {'zfp': 'system-xi-arm.ads'}


class CortexM0P(CortexM0):
    @property
    def name(self):
        return 'cortex-m0p'

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mthumb', '-msoft-float',
                '-mcpu=cortex-m0plus')


class CortexM1(ArmV6MTarget):
    @property
    def name(self):
        return 'cortex-m1'

    @property
    def has_fpu(self):
        return True

    @property
    def use_semihosting_io(self):
        return True

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mthumb', '-msoft-float',
                '-mcpu=cortex-m1')

    @property
    def system_ads(self):
        return {'zfp': 'system-xi-arm.ads'}


class CortexM3(ArmV7MTarget):
    @property
    def name(self):
        return 'cortex-m3'

    @property
    def has_fpu(self):
        return True

    @property
    def use_semihosting_io(self):
        return True

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mthumb', '-msoft-float',
                '-mcpu=cortex-m3')

    @property
    def system_ads(self):
        return {'zfp': 'system-xi-arm.ads',
                'ravenscar-full': 'system-xi-arm-full.ads'}


class CortexM4(ArmV7MTarget):
    @property
    def name(self):
        return 'cortex-m4'

    @property
    def has_fpu(self):
        return True

    @property
    def use_semihosting_io(self):
        return True

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mthumb', '-msoft-float',
                '-mcpu=cortex-m4')

    @property
    def system_ads(self):
        return {'zfp': 'system-xi-arm.ads'}


class CortexM4F(CortexM4):
    @property
    def name(self):
        return 'cortex-m4f'

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mthumb', '-mhard-float',
                '-mcpu=cortex-m4', '-mfpu=fpv4-sp-d16')


class CortexM7F(ArmV7MTarget):
    @property
    def name(self):
        return 'cortex-m7f'

    @property
    def has_fpu(self):
        return True

    @property
    def use_semihosting_io(self):
        return True

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mthumb', '-mhard-float',
                '-mcpu=cortex-m7', '-mfpu=fpv5-sp-d16')

    @property
    def system_ads(self):
        return {'zfp': 'system-xi-arm.ads'}


class CortexM7DF(CortexM7F):
    @property
    def name(self):
        return 'cortex-m7df'

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mthumb', '-mhard-float',
                '-mcpu=cortex-m7', '-mfpu=fpv5-d16')
