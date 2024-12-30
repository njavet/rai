
## Infinity
The set of real numbers is infinite, uncountable, and therefore it is 
impossible to represent all numbers on a finite machine (humans would 
also count as finite machines in my opinion, since I never saw somebody 
computing with "real" real numbers).
For a Basis B ∈ ℕ with B > 1 we can express any real number x ∈ ℝ like this:

x = m * B^e (exponent e ∈ ℤ, m ∈ ℝ)

### Floating point numbers
The set M of machine representable numbers to the Basis B is:

M = {x ∈ ℝ | x = +/- 0.m1m2m3...mn * B ^ (+/- e1e2..el) ∪ {0}

-> TODO ...

### IEEE double precision:
* 64bit numbers 
* 1 sign bit 
* 11 bits for e 
* 52 bits for m
* normalized with 1 before the point, plus 1 bit for the mantissa (hidden bit)
* V = 1 means negative
* bias = 127 bits to save the sign bit of exponent

x = (-1)^V * (1.MMM...MMM) * 2^(E...E) - bias

### Attributes
* Machine numbers are not uniformly distributed
* overflow -> inf
* underflow -> 0
* 1.0 + 1.1102230246251565e-16 == 1.0
 
real numbers: <Ctrl>-v u211d
natural numbers u2115
numbers: u2124

unicode inserts:
in insert mode, press <Ctrl>-v then press u<unicode string>

negation ¬ : <Ctrl>-v u00ac
implication → : <Ctrl>-v u2192
conjunction ∧ : <Ctrl>-v u2227
disjunction ∨ : <Ctrl>-v u2228
bi-implication ↔ : <Ctrl>-v u2194

syntactic identity:
equivalence / identity ≡: <Ctrl>-v u2261

equivalnce ⇔ : <Ctrl>-v u21d4 

All quantor ∀ : <Ctrl>-v u2200
Existence quantor ∃ : <Ctrl>-v u2203
element of ∈ : <Ctrl>-v u2208
subset of ⊆ : <Ctrl>-v u2286
union ∪: <Ctrl>-v u222a
intersection ∩ : <Ctrl>-v u2229

true ⊤ : <Ctrl>-v u22a4
falsity ⊥: <Ctrl>-v u22a5
entailment ⊨ : <Ctrl>-v u22a8
inference  ⊢ : <Ctrl>-v u22a2

