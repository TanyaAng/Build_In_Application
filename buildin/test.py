
RandD = 'RD'
PD = 'PD'
SD = 'SD'
DD = 'DD'
CD = 'CD'
OTHER = 'Other'
PHASES = (
    (RandD, "R&D"),
    (PD, "Preliminary design"),
    (SD, "Schematic Design"),
    (DD, "Design Development"),
    (CD, "Construction Documentation"),
    (OTHER, 'Other')
)
PROJECT_PHASE_MAX_LENGTH = max(len(x) for x ,_ in PHASES)

print(PROJECT_PHASE_MAX_LENGTH)