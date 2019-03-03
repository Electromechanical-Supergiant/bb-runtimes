SVD2ADA_DIR=$(shell dirname $(shell which svd2ada))

.PHONY: svd

all: svd

svd:
	rm -rf */svd */svdtmp
	$(SVD2ADA_DIR)/svd2ada $(SVD2ADA_DIR)/CMSIS-SVD/ATMEL/ATSAM3X8E.svd -p Interfaces.SAM3X8E -o sam3x8e/svdtmp --boolean
	$(SVD2ADA_DIR)/svd2ada $(SVD2ADA_DIR)/CMSIS-SVD/ATMEL/ATSAM4SD32C.svd -p Interfaces.SAM4S -o sam4s/svdtmp --boolean
	$(SVD2ADA_DIR)/svd2ada $(SVD2ADA_DIR)/CMSIS-SVD/ATMEL/ATSAMG55J19.svd -p Interfaces.SAMG55 -o samg55/svdtmp --boolean
	for d in */svdtmp; do \
	  cd $$d; \
	  mkdir ../svd; \
	  mv i-sam*.ads ../svd; \
	  mv i-sam*-efc.ads ../svd; \
	  mv i-sam*-pmc.ads ../svd; \
	  mv i-sam*-sysc.ads ../svd; \
	  mv handler.S ../svd; \
	  mv a-intnam.ads ../svd; \
	  cd ../..; \
	done
	rm -rf */svdtmp
