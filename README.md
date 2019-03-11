# xmlhx
generate a haxe gui code from xml

## features
### field declarations
```
...
<Button width="200" height="200" id="button0"/>
...
```
```
...
private var button0: Button;
...
```
the xmlhx generates field declarations by haxe syntax from all elements in xml file excluded top depth element.  
### field initializations
```
<Application>
    <Label id="question" text="do you like coffee ?"/>
    <HBox id="horizontallayout">
        <Button width="200" height="200" id="button0" label="yes"/>
        <Button width="200" height="200" id="button1" label="no"/>
    </HBox>
</Application>
```
```
private var horizontallayout: HBox;
private var button1: Button;
private var button0: Button;
private var question: Label;
private function initialize(): Void {
	question = new Label();
	question.text = "do you like coffee ?";
	question.id = "question";
	addChild(question);
	horizontallayout = new HBox();
	horizontallayout.id = "horizontallayout";
	addChild(horizontallayout);
	button0 = new Button();
	button0.width = 200;
	button0.height = 200;
	button0.id = "button0";
	button0.label = "yes";
	horizontallayout.addChild(button0);
	button1 = new Button();
	button1.width = 200;
	button1.height = 200;
	button1.id = "button1";
	button1.label = "no";
	horizontallayout.addChild(button1);
}
```
the xmlhx prepares initialization method from xml attribute and bring up tree structure from xml composition structure.
### rules the transcoding from xml to hx
you can specify the advanced settings for xmlhx by config file of xml.
```
<conf>
    <mxml>
        <!-- you can put multiple rules for xml element -->
        <rule>
            <!-- hit xml element by match condition which uses tag condition and attribute condition as AND conditions -->
            <!-- just match tag condition if you put tag element only -->
            <!-- just match attribute condition while attribute element alone -->
            <!-- you must put tag or attribute element here -->
            <match>
                <tag>w</tag>
                <attribute>id</attribute>
            </match>
            <!-- overrides element tag name or attribute when generating gui code. -->
            <!-- the tag element set xml element tag name by specify self text-->
            <!-- the attribute element replace xml element attribute by specify self text -->
            <!-- the style element replace xml element attribute into style field if it appears in supply element-->
            <!-- the quote element surrounds xml element attribute if it appears in supply element -->
            <!-- you must put tag or attribute or style or quote element -->
            <!-- you must put attribute element in match element if you want to use attribute, style, quote in supply -->
            <!-- you must put supply or erase element here, and both supply and erase can not place here-->
            <supply>
                <tag>w</tag>
                <attribute>w</attribute>
                <style/>
                <quote/>
            </supply>
        </rule>
        <rule>
            <match>
                <tag>Button</tag>
                <attribute>w</attribute>
            </match>
            <!-- erases element or its attribute -->
            <!-- the tag element removes out and ignore xml element if it appears here -->
            <!-- the attribute element removes out and ignore xml attribute if it appears here -->
            <!-- you must put tag or attribute element -->
            <erase>
                <tag/>
                <attribute/>
            </erase>
        </rule>
    </mxml>
    <haxe>
        <!-- specify gui coding rules -->
        <!-- the addchild element pushes child into parent gui component by its method such as parent.${addchild}(child); -->
        <!-- the setstyle element puts style such as gui.${setstyle}("${style}",value);; -->
        <!-- the declarefield element make ${id} attribute variable name -->
        <!-- the accessor element declares all fields by its access level -->
        <!-- the initialize element generate initialize components method by its name such as function ${initialize}(): Void{} -->
        <!-- you must put all 5 elements below and keep valid value in text -->
        <rule>
            <addchild>addChild</addchild>
            <setstyle>setStyle</setstyle>
            <declarefield>id</declarefield>
            <accessor>private</accessor>
            <initialize>initialize</initialize>
        </rule>
    </haxe>
</conf>
```
## usages
python xmlhx.py &lt;config file&gt; &lt;xml file&gt;
