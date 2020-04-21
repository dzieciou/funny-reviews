
TODO Paper

    TODO The extended abstract can be structured as a short paper. E.g., it can have sections (e.g. Intro, Method, Experiments, References etc.), it can include images / figures / tables  etc.
    
    
    * Clarity of the description of the paper reproduced
    * Understanding of the paper reproduced
    * Clear description of the reproduction setting / implementation
    * Discuss results of the reproduction
    * Comments on the difficulty of reproducing results / criticisms
    * (bonus) Further exploration of the method, e.g. robustness to hyper-parameters, additional testing on a different dataset, etc.
    
TODO Add to Git


# Pretrain WikiData KB

```cmd
spaCy\bin\wiki_entity_linking\wikidata_pretrain_kb.py D:\Projects-intellij\funny-reviews\data\wiki\latest-all.json.bz2 D:\Projects-intellij\funny-reviews\data\wiki\enwiki-20200201-pages-articles-multistream.xml.bz2 D:\Projects-intellij\funny-reviews\data\kb en_core_web_lg
```

# Setup

## GLOW1 Wikifier

https://cogcomp.seas.upenn.edu/page/download_view/Wikifier

## GLOW2 Wikifier

## 


* Comments on the difficulty of reproducing results / criticisms


 rBugs in the GLOW code:

	Critical warning: word afford is not found in the text 
	Critical warning: word be is not found in the text 
	Critical warning: word even is not found in the text 
	Critical warning: word afford is not found in the text 
	Critical warning: word be is not found in the text 
	Exception in thread "main" java.lang.StringIndexOutOfBoundsException: String index out of range: -1630
		at java.lang.String.substring(String.java:1967)
		at CommonSenseWikifier.Caching.FakeCurator.getLabeling(FakeCurator.java:230)
		at CommonSenseWikifier.Caching.FakeCurator.addNerChunkAndPosSpans(FakeCurator.java:82)
		at CommonSenseWikifier.Caching.CachingCurator.getTextAnnotation(CachingCurator.java:62)
		at Wikifier.wikifyText(Wikifier.java:109)
		at Wikifier.wikifyReviews(Wikifier.java:91)
		at Wikifier.main(Wikifier.java:45)
	
