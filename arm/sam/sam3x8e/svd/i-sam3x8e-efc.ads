--
--  Copyright (C) 2019, AdaCore
--

--  This spec has been automatically generated from ATSAM3X8E.svd

pragma Ada_2012;
pragma Style_Checks (Off);

with System;

package Interfaces.SAM3X8E.EFC is
   pragma Preelaborate;
   pragma No_Elaboration_Code_All;

   ---------------
   -- Registers --
   ---------------

   subtype EFC0_FMR_FRDY_Field is Interfaces.SAM3X8E.Bit;
   subtype EFC0_FMR_FWS_Field is Interfaces.SAM3X8E.UInt4;
   subtype EFC0_FMR_SCOD_Field is Interfaces.SAM3X8E.Bit;
   subtype EFC0_FMR_FAM_Field is Interfaces.SAM3X8E.Bit;

   --  EEFC Flash Mode Register
   type EFC0_FMR_Register is record
      --  Ready Interrupt Enable
      FRDY           : EFC0_FMR_FRDY_Field := 16#0#;
      --  unspecified
      Reserved_1_7   : Interfaces.SAM3X8E.UInt7 := 16#0#;
      --  Flash Wait State
      FWS            : EFC0_FMR_FWS_Field := 16#0#;
      --  unspecified
      Reserved_12_15 : Interfaces.SAM3X8E.UInt4 := 16#0#;
      --  Sequential Code Optimization Disable
      SCOD           : EFC0_FMR_SCOD_Field := 16#0#;
      --  unspecified
      Reserved_17_23 : Interfaces.SAM3X8E.UInt7 := 16#0#;
      --  Flash Access Mode
      FAM            : EFC0_FMR_FAM_Field := 16#0#;
      --  unspecified
      Reserved_25_31 : Interfaces.SAM3X8E.UInt7 := 16#0#;
   end record
     with Volatile_Full_Access, Object_Size => 32,
          Bit_Order => System.Low_Order_First;

   for EFC0_FMR_Register use record
      FRDY           at 0 range 0 .. 0;
      Reserved_1_7   at 0 range 1 .. 7;
      FWS            at 0 range 8 .. 11;
      Reserved_12_15 at 0 range 12 .. 15;
      SCOD           at 0 range 16 .. 16;
      Reserved_17_23 at 0 range 17 .. 23;
      FAM            at 0 range 24 .. 24;
      Reserved_25_31 at 0 range 25 .. 31;
   end record;

   --  Flash Command
   type FCR_FCMD_Field is
     (--  Get Flash Descriptor
      Getd,
      --  Write page
      Wp,
      --  Write page and lock
      Wpl,
      --  Erase page and write page
      Ewp,
      --  Erase page and write page then lock
      Ewpl,
      --  Erase all
      Ea,
      --  Set Lock Bit
      Slb,
      --  Clear Lock Bit
      Clb,
      --  Get Lock Bit
      Glb,
      --  Set GPNVM Bit
      Sgpb,
      --  Clear GPNVM Bit
      Cgpb,
      --  Get GPNVM Bit
      Ggpb,
      --  Start Read Unique Identifier
      Stui,
      --  Stop Read Unique Identifier
      Spui,
      --  Get CALIB Bit
      Gcalb)
     with Size => 8;
   for FCR_FCMD_Field use
     (Getd => 0,
      Wp => 1,
      Wpl => 2,
      Ewp => 3,
      Ewpl => 4,
      Ea => 5,
      Slb => 8,
      Clb => 9,
      Glb => 10,
      Sgpb => 11,
      Cgpb => 12,
      Ggpb => 13,
      Stui => 14,
      Spui => 15,
      Gcalb => 16);

   subtype EFC0_FCR_FARG_Field is Interfaces.SAM3X8E.UInt16;

   --  Flash Writing Protection Key
   type FCR_FKEY_Field is
     (--  Reset value for the field
      Fcr_Fkey_Field_Reset,
      --  The 0x5A value enables the command defined by the bits of the register. If
--  the field is written with a different value, the write is not performed and
--  no action is started.
      Passwd)
     with Size => 8;
   for FCR_FKEY_Field use
     (Fcr_Fkey_Field_Reset => 0,
      Passwd => 90);

   --  EEFC Flash Command Register
   type EFC0_FCR_Register is record
      --  Write-only. Flash Command
      FCMD : FCR_FCMD_Field := Interfaces.SAM3X8E.EFC.Getd;
      --  Write-only. Flash Command Argument
      FARG : EFC0_FCR_FARG_Field := 16#0#;
      --  Write-only. Flash Writing Protection Key
      FKEY : FCR_FKEY_Field := Fcr_Fkey_Field_Reset;
   end record
     with Volatile_Full_Access, Object_Size => 32,
          Bit_Order => System.Low_Order_First;

   for EFC0_FCR_Register use record
      FCMD at 0 range 0 .. 7;
      FARG at 0 range 8 .. 23;
      FKEY at 0 range 24 .. 31;
   end record;

   subtype EFC0_FSR_FRDY_Field is Interfaces.SAM3X8E.Bit;
   subtype EFC0_FSR_FCMDE_Field is Interfaces.SAM3X8E.Bit;
   subtype EFC0_FSR_FLOCKE_Field is Interfaces.SAM3X8E.Bit;

   --  EEFC Flash Status Register
   type EFC0_FSR_Register is record
      --  Read-only. Flash Ready Status
      FRDY          : EFC0_FSR_FRDY_Field;
      --  Read-only. Flash Command Error Status
      FCMDE         : EFC0_FSR_FCMDE_Field;
      --  Read-only. Flash Lock Error Status
      FLOCKE        : EFC0_FSR_FLOCKE_Field;
      --  unspecified
      Reserved_3_31 : Interfaces.SAM3X8E.UInt29;
   end record
     with Volatile_Full_Access, Object_Size => 32,
          Bit_Order => System.Low_Order_First;

   for EFC0_FSR_Register use record
      FRDY          at 0 range 0 .. 0;
      FCMDE         at 0 range 1 .. 1;
      FLOCKE        at 0 range 2 .. 2;
      Reserved_3_31 at 0 range 3 .. 31;
   end record;

   -----------------
   -- Peripherals --
   -----------------

   --  Embedded Flash Controller 0
   type EFC_Peripheral is record
      --  EEFC Flash Mode Register
      FMR : aliased EFC0_FMR_Register;
      --  EEFC Flash Command Register
      FCR : aliased EFC0_FCR_Register;
      --  EEFC Flash Status Register
      FSR : aliased EFC0_FSR_Register;
      --  EEFC Flash Result Register
      FRR : aliased Interfaces.SAM3X8E.UInt32;
   end record
     with Volatile;

   for EFC_Peripheral use record
      FMR at 16#0# range 0 .. 31;
      FCR at 16#4# range 0 .. 31;
      FSR at 16#8# range 0 .. 31;
      FRR at 16#C# range 0 .. 31;
   end record;

   --  Embedded Flash Controller 0
   EFC0_Periph : aliased EFC_Peripheral
     with Import, Address => EFC0_Base;

   --  Embedded Flash Controller 1
   EFC1_Periph : aliased EFC_Peripheral
     with Import, Address => EFC1_Base;

end Interfaces.SAM3X8E.EFC;
