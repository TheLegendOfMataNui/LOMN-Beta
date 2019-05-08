SHELL = cmd
BLKTOOL = python tools\blkfile.py
COMPRESSION = decompressed # can also set to compressed
BLKARGS = --$(COMPRESSION)
OSATOOL = sage-js
OSAARGS = res:osi:asm:sassemble
BLOCKFILES = Main.blk Art/Art.blk characters/msqt.blk characters/wind.blk characters/gali.blk characters/tahu.blk characters/lewa.blk characters/mudm.blk characters/rptl.blk characters/rrun.blk characters/bats.blk characters/sfsh.blk characters/ibat.blk characters/oewa.blk characters/dfly.blk characters/bspd.blk characters/imon.blk characters/pira.blk characters/spid.blk characters/vine.blk characters/tspd.blk characters/crb1.blk characters/vlgr.blk characters/lsrp.blk characters/hydr.blk characters/turt.blk characters/shrk.blk characters/ttrt.blk characters/onua.blk characters/tfsh.blk characters/bull.blk characters/nUju.blk characters/btfr.blk characters/Textures.blk characters/bugz.blk characters/vaka.blk characters/wrat.blk characters/ssss.blk characters/drag.blk characters/bsrp.blk characters/kopa.blk characters/poha.blk characters/mata.blk characters/rkmn.blk characters/noka.blk characters/fbug.blk characters/when.blk Languages/lang_swe.blk Languages/lang_dan.blk Languages/lang_dut.blk Languages/lang_spa.blk Languages/lang_frn.blk Languages/lang_eng.blk Languages/lang_ger.blk Languages/lang_ita.blk Sounds/sounds.blk Art/PrinterPics/printerart.blk levels/fren/frnt.blk levels/fren/fren.blk levels/lev0/frnt.blk levels/lev0/lev0.blk levels/lev1/atrm.blk levels/lev1/bech.blk levels/lev1/ptv1.blk levels/lev1/bugs.blk levels/lev1/l1a8.blk levels/lev1/l1a1.blk levels/lev1/pzzl.blk levels/lev1/vllg.blk levels/lev1/scrp.blk levels/lev1/clf2.blk levels/lev1/shrn.blk levels/lev1/lev1.blk levels/lev1/spcv.blk levels/lev1/tura.blk levels/lev1/l1a3.blk levels/lev1/cave.blk levels/lev1/hk01.blk levels/lev1/clf1.blk levels/lev1/mud0.blk levels/lev1/l1a7.blk levels/lev2/vtnl.blk levels/lev2/strt.blk levels/lev2/wthk.blk levels/lev2/mwat.blk levels/lev2/vllg.blk levels/lev2/lev2.blk levels/lev2/hydr.blk levels/lev2/takv.blk levels/lev2/vlgs.blk levels/lev2/evac.blk levels/lev2/tura.blk levels/lev2/mtop.blk levels/lev2/ttun.blk levels/lev2/mtup.blk levels/lev2/gly3.blk levels/lev2/hk01.blk levels/lev2/ghut.blk levels/lev2/shrn.blk levels/lev3/lev3.blk levels/lev3/gly1.blk levels/lev3/blr2.blk levels/lev3/bkik.blk levels/lev3/vllg.blk levels/lev3/boss.blk levels/lev3/blr1.blk levels/lev3/blcv.blk levels/lev3/xrod.blk levels/lev3/tura.blk levels/lev3/rkfl.blk levels/lev3/hutt.blk levels/lev3/mtup.blk levels/lev3/gly3.blk levels/lev3/bldr.blk levels/lev3/ptos.blk levels/lev3/shrn.blk levels/lev4/visn.blk levels/lev4/well.blk levels/lev4/strt.blk levels/lev4/brd4.blk levels/lev4/path.blk levels/lev4/gly1.blk levels/lev4/mosh.blk levels/lev4/swrd.blk levels/lev4/snfl.blk levels/lev4/vllg.blk levels/lev4/boss.blk levels/lev4/lev4.blk levels/lev4/haka.blk levels/lev4/Tele.blk levels/lev4/crss.blk levels/lev4/brd2.blk levels/lev4/lev4c.blk levels/lev4/maz2.blk levels/lev4/hutt.blk levels/lev4/icmz.blk levels/lev4/brd3.blk levels/lev4/maz1.blk levels/lev4/tura.blk levels/lev4/shrn.blk levels/lev4/snbd.blk levels/lev5/lev5.blk levels/lev5/le03.blk levels/lev5/le04.blk levels/lev5/gly1.blk levels/lev5/hive.blk levels/lev5/vllg.blk levels/lev5/boss.blk levels/lev5/lep1.blk levels/lev5/le08.blk levels/lev5/shrn.blk levels/lev5/le02.blk levels/lev5/mtup.blk levels/lev5/lep2.blk levels/lev5/tura.blk levels/lev5/room.blk levels/lev5/le01.blk levels/lev5/cave.blk levels/lev5/gly3.blk levels/lev6/ta08.blk levels/lev6/ta12.blk levels/lev6/ta05.blk levels/lev6/fvil.blk levels/lev6/vllg.blk levels/lev6/ta02.blk levels/lev6/ta11.blk levels/lev6/boss.blk levels/lev6/ta14.blk levels/lev6/tvil.blk levels/lev6/shrn.blk levels/lev6/ta07.blk levels/lev6/tp02.blk levels/lev6/ta01.blk levels/lev6/ta13.blk levels/lev6/ta04.blk levels/lev6/tura.blk levels/lev6/lev6.blk levels/lev6/hutt.blk levels/lev6/tp01.blk levels/lev6/mtup.blk levels/lev6/ta03.blk levels/lev6/ta09.blk levels/lev7/tahu.blk levels/lev7/lewa.blk levels/lev7/phtu.blk levels/lev7/onua.blk levels/lev7/lev7.blk levels/lev7/kpka.blk levels/lev7/gali.blk
NATIVE_SOURCES = $(wildcard ./native/*.*) $(wildcard ./native/*/*.*)
NATIVE_OUTPUTS = $(patsubst ./native/%,./build/%, $(NATIVE_SOURCES))
OSI_SOURCES = $(wildcard ./script/*.osas) $(wildcard ./script/*/*.osas)
OSI_OUTPUT = ./build/data/Base.osi

default: build

build: native script data blockfiles

clean:
	@if exist build\NUL rmdir build /s /q

run: build
	@start build\LEGOBionicle.exe

rebuild:
	@$(MAKE) -s clean
	@$(MAKE) -s build

.PHONY: extract

# 
# Utility recipe for extracting existing blockfiles.
# 
extract: $(addsuffix .tmp,$(addprefix ./blockfiles/,$(basename $(BLOCKFILES))))

./blockfiles/%.tmp:
	@echo Blockfile: $(addsuffix .blk,$(basename $@))
	@if exist $(subst /,\,$(basename $@))\NUL rmdir $(subst /,\,$(basename $@)) /s /q
	@$(BLKTOOL) $(addsuffix .blk,$(basename $@)) > /dev/null

# 
# Native files copied from native/
# 
native: $(NATIVE_OUTPUTS)

./build/%: ./native/%
	@echo Copying '$@'...
	@if not exist $(subst /,\,$(dir $@))NUL mkdir $(subst /,\,$(dir $@))
	@copy /B $(subst /,\,$<) $(strip $(subst /,\,$@)) > NUL

# 
# Script files are compiled from script/ with sage-js
# 
script: $(OSI_OUTPUT)

$(OSI_OUTPUT): $(OSI_SOURCES)
	@echo Compiling '$@'...
	@if not exist $(subst /,\,$(dir $@))NUL mkdir $(subst /,\,$(dir $@))
	@$(OSATOOL) $(OSAARGS) $(subst /,\,$@) ./script/

# 
# Data files are copied from data/
# 
DATA_SOURCES = $(wildcard ./data/*.*) $(wildcard ./data/*/*.*) $(wildcard ./data/*/*/*.*) $(wildcard ./data/*/*/*/*.*) $(wildcard ./data/*/*/*/*/*.*) $(wildcard ./data/*/*/*/*/*/*.*)
DATA_OUTPUTS = $(patsubst ./data/%,./build/data/%,$(DATA_SOURCES))
data: $(DATA_OUTPUTS)

./build/data/%: ./data/%
	@echo Copying '$@'...
	@if not exist $(subst /,\,$(dir $@))NUL mkdir $(subst /,\,$(dir $@))
	@copy /B $(subst /,\,$<) $(strip $(subst /,\,$@)) > NUL

# 
# Blockfiles are packaged from blockfiles/ with blkfile.py
# 
blockfiles: $(addprefix ./build/data/,$(BLOCKFILES))

.SECONDEXPANSION:

./build/data/%.blk: $$(wildcard ./blockfiles/%/*.*)
	@echo Packaging '$@'...
	@if not exist $(subst /,\,$(dir $@))NUL mkdir $(subst /,\,$(dir $@))
	@if not exist $(subst /,\,$(patsubst build/data/%.blk,./blockfiles/%,$@))NUL mkdir $(subst /,\,$(patsubst build/data/%.blk,./blockfiles/%,$@))
	@if exist $(subst /,\,$@) rm $(subst /,\,$@)
	@$(BLKTOOL) $(BLKARGS) -o $@ $(patsubst build/data/%.blk,./blockfiles/%,$@) > NUL
