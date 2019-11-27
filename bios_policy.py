## BASE MODULES ##
import sys
import re
import argparse
import socket
from getpass import getpass

## UCSM HANDLE ##
from ucsmsdk.ucshandle import UcsHandle

## BIOS PROFILE OBJECT ##
from ucsmsdk.mometa.bios.BiosVProfile import BiosVProfile

## MAIN OBJECTS ##
from ucsmsdk.mometa.bios.BiosVfConsistentDeviceNameControl import BiosVfConsistentDeviceNameControl
from ucsmsdk.mometa.bios.BiosVfFrontPanelLockout import BiosVfFrontPanelLockout
from ucsmsdk.mometa.bios.BiosVfPOSTErrorPause import BiosVfPOSTErrorPause
from ucsmsdk.mometa.bios.BiosVfQuietBoot import BiosVfQuietBoot
from ucsmsdk.mometa.bios.BiosVfResumeOnACPowerLoss import BiosVfResumeOnACPowerLoss

## ADVANCED PROCESSOR OBJECTS ##
from ucsmsdk.mometa.bios.BiosVfAltitude import BiosVfAltitude
from ucsmsdk.mometa.bios.BiosVfCPUHardwarePowerManagement import BiosVfCPUHardwarePowerManagement
# Boot Performance Mode (Max Performance)
from ucsmsdk.mometa.bios.BiosVfCPUPerformance import BiosVfCPUPerformance
from ucsmsdk.mometa.bios.BiosVfCoreMultiProcessing import BiosVfCoreMultiProcessing
from ucsmsdk.mometa.bios.BiosVfDRAMClockThrottling import BiosVfDRAMClockThrottling
from ucsmsdk.mometa.bios.BiosVfDirectCacheAccess import BiosVfDirectCacheAccess
from ucsmsdk.mometa.bios.BiosVfEnergyPerformanceTuning import BiosVfEnergyPerformanceTuning
from ucsmsdk.mometa.bios.BiosVfEnhancedIntelSpeedStepTech import BiosVfEnhancedIntelSpeedStepTech
from ucsmsdk.mometa.bios.BiosVfExecuteDisableBit import BiosVfExecuteDisableBit
from ucsmsdk.mometa.bios.BiosVfFrequencyFloorOverride import BiosVfFrequencyFloorOverride
from ucsmsdk.mometa.bios.BiosVfIntelHyperThreadingTech import BiosVfIntelHyperThreadingTech
# Energy Efficient Turbo (Disabled)
from ucsmsdk.mometa.bios.BiosVfIntelTurboBoostTech import BiosVfIntelTurboBoostTech
from ucsmsdk.mometa.bios.BiosVfIntelVirtualizationTechnology import BiosVfIntelVirtualizationTechnology
from ucsmsdk.mometa.bios.BiosVfInterleaveConfiguration import BiosVfInterleaveConfiguration
# IMC Interleave (Auto)
# Sub NUMA Clustering (Disabled)
from ucsmsdk.mometa.bios.BiosVfLocalX2Apic import BiosVfLocalX2Apic
from ucsmsdk.mometa.bios.BiosVfMaxVariableMTRRSetting import BiosVfMaxVariableMTRRSetting
from ucsmsdk.mometa.bios.BiosVfPSTATECoordination import BiosVfPSTATECoordination
from ucsmsdk.mometa.bios.BiosVfPackageCStateLimit import BiosVfPackageCStateLimit
# Autonomous Core C-State (Disabled)
from ucsmsdk.mometa.bios.BiosVfProcessorCState import BiosVfProcessorCState
from ucsmsdk.mometa.bios.BiosVfProcessorC1E import BiosVfProcessorC1E
from ucsmsdk.mometa.bios.BiosVfProcessorC3Report import BiosVfProcessorC3Report
from ucsmsdk.mometa.bios.BiosVfProcessorC6Report import BiosVfProcessorC6Report
from ucsmsdk.mometa.bios.BiosVfProcessorC7Report import BiosVfProcessorC7Report
from ucsmsdk.mometa.bios.BiosVfProcessorCMCI import BiosVfProcessorCMCI
from ucsmsdk.mometa.bios.BiosVfProcessorEnergyConfiguration import BiosVfProcessorEnergyConfiguration
# ProcessorEppProfile (Balanced Performance)*
from ucsmsdk.mometa.bios.BiosVfProcessorPrefetchConfig import BiosVfProcessorPrefetchConfig
# UPI Prefetch (Enabled)
# LLC Prefetch (Disabled)
# XPT Prefetch (Disabled)*
# Core Performance Boost (Auto)^
# Downcore Control (Auto)^
# Global C-State Control (Auto)^
# L1 Stream HW Prefetcher (Auto)^
# L2 Stream HW Prefetcher (Auto)^
# Determinism Slider (Auto)^
# IOMMU (Auto)^
# Bank Group Swap (Auto)^
# Chipselect Interleaving (Auto)^
# AMD Memory Interleaving (Auto)^
# AMD Memory Interleaving Size (Auto)^
# SMEE (Enabled)^
# SMT Mode (Auto)^
# SVM Mode (Enabled)^
from ucsmsdk.mometa.bios.BiosVfScrubPolicies import BiosVfScrubPolicies
from ucsmsdk.mometa.bios.BiosVfWorkloadConfiguration import BiosVfWorkloadConfiguration

## ADVANCED INTEL DIRECTED IO OBJECTS ##
from ucsmsdk.mometa.bios.BiosVfIntelVTForDirectedIO import BiosVfIntelVTForDirectedIO

## ADVANCED RAS MEMORY OBJECTS ##
from ucsmsdk.mometa.bios.BiosVfDDR3VoltageSelection import BiosVfDDR3VoltageSelection
from ucsmsdk.mometa.bios.BiosVfDramRefreshRate import BiosVfDramRefreshRate
from ucsmsdk.mometa.bios.BiosVfLvDIMMSupport import BiosVfLvDIMMSupport
from ucsmsdk.mometa.bios.BiosVfMirroringMode import BiosVfMirroringMode
from ucsmsdk.mometa.bios.BiosVfNUMAOptimized import BiosVfNUMAOptimized
from ucsmsdk.mometa.bios.BiosVfSelectMemoryRASConfiguration import BiosVfSelectMemoryRASConfiguration

# Arg Parser Config
arg_parser = argparse.ArgumentParser(prog='bios_policy', description='Create a New UCSM BIOS Policy')
arg_parser.version = '1.0'
arg_parser.add_argument('-a', dest="address", action='store', help='FQDN or IP Address for UCSM', metavar='ADDR', required=False)
arg_parser.add_argument('-n', dest="name", action='store', help='Name of the New BIOS Policy', metavar='NAME', required=False)
arg_parser.add_argument('-u', dest='user', action='store', help='UCSM Username', metavar='USER', required=False)
arg_parser.add_argument('-p', dest='pwd', action='store', help='UCSM Password', metavar='PASS', required=False)
arg_parser.add_argument('-t', dest='thread', action='store_true', help='Enable HyperThreading')
arg_parser.add_argument('-v', action='version', help='Show Version')
args = arg_parser.parse_args()

# Get UCSM FQDN/IP if not Provided as an Argument
if args.address == None:
    ucsm_addr = input("UCSM FQDN/IP Address: ")
else:
    ucsm_addr = args.address

# Make sure UCSM FQDN/IP isn't Blank
if ucsm_addr == "":
    print("Invalid UCSM FQDN/IP Address!")
    sys.exit(1)

# Check if UCSM FQDN/IP is Valid
try:
    socket.gethostbyname(ucsm_addr)
except socket.gaierror:
    print("Invalid UCSM FQDN/IP Address!")
    sys.exit(1)

# Get New Policy Name if not Provided as an Argument
if args.name == None:
    policy_name = input("New BIOS Policy Name: ")
else:
    policy_name = args.name

# Verify that New BIOS Policy Name is Valid
regex_check = re.search('^(\\w|[.:_-]){1,16}$', policy_name)

if not regex_check:
    print("Invalid UCSM BIOS Policy Name!")
    sys.exit(1)

# Get UCSM Username if not Provided as an Argument
if args.user == None:
    user_name = input("UCSM username: ")
else:
    user_name = args.user

# Get UCSM Password if not Provided as an Argument
if args.pwd == None:
    user_pass = getpass("UCSM password: ")
else:
    user_pass = args.pwd

print()

# Create UCSM Handle
handle = UcsHandle(ucsm_addr, user_name, user_pass)

# Log Into UCSM
print("Logging into UCSM...", end='')
login_result = handle.login()

if(login_result):
    print("SUCCESS!")
else:
    print("FAILED!")

# Create Base BIOS Profile
mo = BiosVProfile(parent_mo_or_dn="org-root", name="test-bios")

# Modify Main Objects
cdn_control = BiosVfConsistentDeviceNameControl(parent_mo_or_dn=mo, vp_cdn_control="platform-default")
front_panel_lockout = BiosVfFrontPanelLockout(parent_mo_or_dn=mo, vp_front_panel_lockout="platform-default")
post_error_pause = BiosVfPOSTErrorPause(parent_mo_or_dn=mo, vp_post_error_pause="platform-default")
quiet_boot = BiosVfQuietBoot(parent_mo_or_dn=mo, vp_quiet_boot="platform-default")
resume_on_power_loss = BiosVfResumeOnACPowerLoss(parent_mo_or_dn=mo, vp_resume_on_ac_power_loss="platform-default")

# Modify Advanced Processor Objects
altitude = BiosVfAltitude(parent_mo_or_dn=mo, vp_altitude="platform-default")
power_management = BiosVfCPUHardwarePowerManagement(parent_mo_or_dn=mo, vp_cpu_hardware_power_management="disabled")
# Boot Performance Mode
cpu_performance = BiosVfCPUPerformance(parent_mo_or_dn=mo, vp_cpu_performance="enterprise")
core_multi_processing = BiosVfCoreMultiProcessing(parent_mo_or_dn=mo, vp_core_multi_processing="all")
dram_clock_throttling = BiosVfDRAMClockThrottling(parent_mo_or_dn=mo, vp_dram_clock_throttling="performance")
direct_cache_access = BiosVfDirectCacheAccess(parent_mo_or_dn=mo, vp_direct_cache_access="platform-default")
energy_performance_tuning = BiosVfEnergyPerformanceTuning(parent_mo_or_dn=mo, vp_pwr_perf_tuning="os")
enhanced_intel_speedstep_tech = BiosVfEnhancedIntelSpeedStepTech(parent_mo_or_dn=mo, vp_enhanced_intel_speed_step_tech="platform-default")
execute_disable_bit = BiosVfExecuteDisableBit(parent_mo_or_dn=mo, vp_execute_disable_bit="platform-default")
frequency_floor_override = BiosVfFrequencyFloorOverride(parent_mo_or_dn=mo, vp_frequency_floor_override="platform-default")

# Special HyperThreading Check
if args.thread == True:
    hyper_threading = BiosVfIntelHyperThreadingTech(parent_mo_or_dn=mo, vp_intel_hyper_threading_tech="enabled")
else:
    hyper_threading = BiosVfIntelHyperThreadingTech(parent_mo_or_dn=mo, vp_intel_hyper_threading_tech="disabled")

# Energy Efficient Turbo
intel_turbo_boost_tech = BiosVfIntelTurboBoostTech(parent_mo_or_dn=mo, vp_intel_turbo_boost_tech="platform-default")
intel_virtualization_technology = BiosVfIntelVirtualizationTechnology(parent_mo_or_dn=mo, vp_intel_virtualization_technology="disabled")
memory_interleaving = BiosVfInterleaveConfiguration(parent_mo_or_dn=mo, vp_channel_interleaving="auto", vp_memory_interleaving="platform-default", vp_rank_interleaving="platform-default")
# IMC Interleave
# Sub NUMA Clustering
local_x2_apic = BiosVfLocalX2Apic(parent_mo_or_dn=mo, vp_local_x2_apic="platform-default")
max_variable_mtrr_setting = BiosVfMaxVariableMTRRSetting(parent_mo_or_dn=mo, vp_processor_mtrr="platform-default")
p_state_coordination = BiosVfPSTATECoordination(parent_mo_or_dn=mo, vp_pstate_coordination="hw-all")
package_c_state_limit = BiosVfPackageCStateLimit(parent_mo_or_dn=mo, vp_package_c_state_limit="c0")
# Autonomous Core C-State
processor_c_state = BiosVfProcessorCState(parent_mo_or_dn=mo, vp_processor_c_state="disabled")
processor_c1e = BiosVfProcessorC1E(parent_mo_or_dn=mo, vp_processor_c1_e="disabled")
processor_c3_report = BiosVfProcessorC3Report(parent_mo_or_dn=mo, vp_processor_c3_report="disabled")
processor_c6_report = BiosVfProcessorC6Report(parent_mo_or_dn=mo, vp_processor_c6_report="disabled")
processor_c7_report = BiosVfProcessorC7Report(parent_mo_or_dn=mo, vp_processor_c7_report="disabled")
processor_cmci = BiosVfProcessorCMCI(parent_mo_or_dn=mo, vp_processor_cmci="platform-default")
energy_performance = BiosVfProcessorEnergyConfiguration(parent_mo_or_dn=mo, vp_power_technology="performance", vp_energy_performance="performance")
# ProcessorEppProfile
prefetch_config = BiosVfProcessorPrefetchConfig(parent_mo_or_dn=mo, vp_adjacent_cache_line_prefetcher="enabled", vp_dcuip_prefetcher="enabled", vp_dcu_streamer_prefetch="enabled", vp_hardware_prefetcher="enabled")
# UPI Prefetch
# LLC Prefetch
# XPT PRefetch
# Core Performance Boost
# Downcore Control
# Global C-State Control
# L1 Stream HW Prefetcher
# L2 Stream HW Prefetcher
# Determinism Slider
# IOMMU
# Bank Group Swap
# Chipselect Interleaving
# AMD Memory Interleaving
# AMD Memory Interleaving Size
# SMEE
# SMT Mode
# SVM Mode
scrub_policies = BiosVfScrubPolicies(parent_mo_or_dn=mo, vp_demand_scrub="platform-default", vp_patrol_scrub="platform-default")
workload_configuration = BiosVfWorkloadConfiguration(parent_mo_or_dn=mo, vp_workload_configuration="balanced")

# Modify Intel Directed IO Objects
intel_vtd = BiosVfIntelVTForDirectedIO(parent_mo_or_dn=mo, vp_intel_vtdats_support="platform-default", vp_intel_vtd_coherency_support="platform-default", vp_intel_vtd_interrupt_remapping="platform-default", vp_intel_vtd_pass_through_dma_support="platform-default", vp_intel_vt_for_directed_io="platform-default")

# Modify RAS Memory Objects
ddr3_voltage = BiosVfDDR3VoltageSelection(parent_mo_or_dn=mo, vp_dd_r3_voltage_selection="platform-default")
dram_refresh_rate = BiosVfDramRefreshRate(parent_mo_or_dn=mo, vp_dram_refresh_rate="1x")
lv_ddr_mode = BiosVfLvDIMMSupport(parent_mo_or_dn=mo, vp_lv_ddr_mode="performance-mode")
mirroring_mode = BiosVfMirroringMode(parent_mo_or_dn=mo, vp_mirroring_mode="platform-default")
numa_optimized = BiosVfNUMAOptimized(parent_mo_or_dn=mo, vp_numa_optimized="enabled")
memory_ras_config = BiosVfSelectMemoryRASConfiguration(parent_mo_or_dn=mo, vp_select_memory_ras_configuration="maximum-performance")

# Create BIOS Policy in UCSM
print("Creating BIOS Policy...", end='')
# handle.add_mo(mo)

try:
    handle.commit()
except:
    print("ERROR!")

print("SUCCESS!")

# Log Out of UCSM
print("Logging out of UCSM...", end='')
logout_result = handle.logout()

if(logout_result):
    print("SUCCESS!")
else:
    print("FAILED!")
