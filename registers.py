# registers.py
# SX1276/SX1278 register map and constants

# Common Register Addresses
REG_FIFO                    = 0x00
REG_OP_MODE                = 0x01

# Frequency Registers
REG_FRF_MSB                = 0x06
REG_FRF_MID                = 0x07
REG_FRF_LSB                = 0x08

# PA config
REG_PA_CONFIG              = 0x09
REG_PA_RAMP                = 0x0A

# OCP (Over Current Protection)
REG_OCP                    = 0x0B

# LNA config
REG_LNA                    = 0x0C

# FIFO Address Pointers
REG_FIFO_ADDR_PTR          = 0x0D
REG_FIFO_TX_BASE_ADDR      = 0x0E
REG_FIFO_RX_BASE_ADDR      = 0x0F
REG_FIFO_RX_CURRENT_ADDR   = 0x10

# IRQ flags
REG_IRQ_FLAGS_MASK         = 0x11
REG_IRQ_FLAGS              = 0x12

# Packet settings
REG_RX_NB_BYTES            = 0x13
REG_PKT_SNR_VALUE          = 0x19
REG_PKT_RSSI_VALUE         = 0x1A
REG_RSSI_VALUE             = 0x1B

# Modem config
REG_MODEM_CONFIG_1         = 0x1D
REG_MODEM_CONFIG_2         = 0x1E
REG_SYMB_TIMEOUT_LSB       = 0x1F
REG_PREAMBLE_MSB           = 0x20
REG_PREAMBLE_LSB           = 0x21
REG_PAYLOAD_LENGTH         = 0x22
REG_MODEM_CONFIG_3         = 0x26

# Frequency Error
REG_FREQ_ERROR_MSB         = 0x28
REG_FREQ_ERROR_MID         = 0x29
REG_FREQ_ERROR_LSB         = 0x2A

# LoRa detection
REG_DETECTION_OPTIMIZE     = 0x31
REG_INVERTIQ               = 0x33
REG_DETECTION_THRESHOLD    = 0x37
REG_SYNC_WORD              = 0x39
REG_INVERTIQ2              = 0x3B

# DIO mapping
REG_DIO_MAPPING_1          = 0x40
REG_DIO_MAPPING_2          = 0x41

# Version
REG_VERSION                = 0x42

# PA Dac
REG_PA_DAC                 = 0x4D

# ------------------------------------------------------------------

# Modes
MODE_SLEEP                 = 0x00
MODE_STDBY                 = 0x01
MODE_TX                    = 0x03
MODE_RX_CONTINUOUS         = 0x05
MODE_RX_SINGLE             = 0x06
MODE_LONG_RANGE_MODE       = 0x80  # LoRa mode bit

# IRQ Masks
IRQ_TX_DONE_MASK           = 0x08
IRQ_RX_DONE_MASK           = 0x40
IRQ_PAYLOAD_CRC_ERROR_MASK = 0x20

# PA config values
PA_BOOST                   = 0x80  # For high power (PA_BOOST pin)

