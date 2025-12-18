# BAC Spec Processor Test Generation Instructions

## Overview

This instruction file guides the generation of unit test classes for BAC (Business Analytics Collection) spec processors.  The tests focus on validating JAXB BACSpec conversion to collection specifications, ensuring proper category handling, list processing, and conversion method functionality.

**Target Pattern**: `BAC{ObjectType}SpecProcessorTest. java`
**Example**:  `BACWTChangeOrder2SpecProcessorTest.java`

## Directory Configuration

- **Package Structure**: `wt.{domain}.bac`
- **Test Location**: Same package as the spec processor class
- **Naming Convention**: `{SpecProcessorClassName}Test.java`
- `object.json` = `c:/FINAL/.github/object.json`

## Read Information from object.json
- **Object Type**: Extract the Windchill object type for spec processing`
- **Collect all field of Object**: Extract all fields related to the object type for test generation

## Delegate Access

BAC spec processors typically implement these core interfaces:  
- Collection category management via `setCollnCategory(CollectionCategory)`
- JAXB processing via `process(BACSpec, ArrayList<BACCollectionSpec>, ArrayList<BACRawCollectionSpec>)`
- Collection spec conversion via `convertJaxbToCollectionSpec(BACSpec)`
- Raw collection spec conversion via `convertJaxbToRawCollectionSpec(BACSpec)`
- Spec list population and management

## Analysis Workflow

1. **Identify Object Type**: Determine the Windchill object type for spec processing
2. **Validate Collection Category**:  Ensure proper CollectionCategory enum usage
3. **Test JAXB Conversion**:  Verify conversion from BACSpec to collection specifications
4. **Test List Processing**: Validate spec list population and manipulation
5. **Test Edge Cases**: Handle null parameters, empty lists, and boundary conditions
6. **Verify Interface Implementation**:  Confirm proper interface implementation

## Object Dependencies and Attributes Extraction

### Core Spec Processing Components:  
- BACSpec (JAXB specification object)
- BACCollectionSpec (processed collection specification)
- BACRawCollectionSpec (raw collection specification)
- CollectionCategory enum values
- ArrayList containers for spec collections

### Spec Processing Patterns:
- JAXB object conversion and transformation
- Collection category assignment and validation
- List population and management
- Multiple invocation consistency
- Thread safety considerations

## Delegate Test Class Generation Steps

### 1. Class Structure Setup
```java
public class BAC{ObjectType}SpecProcessorTest {
    private BAC{ObjectType}SpecProcessor specProcessor;
    private BACSpec bacSpec;
    private ArrayList<BACCollectionSpec> specList;
    private ArrayList<BACRawCollectionSpec> rawSpecList;
}
```

### 2. Test Setup Method
```java
@Before
public void setUp() {
    specProcessor = new BAC{ObjectType}SpecProcessor();
    bacSpec = new BACSpec();
    specList = new ArrayList<>();
    rawSpecList = new ArrayList<>();
}
```

### 3. Core Test Methods
Generate tests for each core method following the patterns below.  

## Delegates Guidelines

### Core Methods to Test

#### Constructor Tests
- **testConstructor**: Verify proper initialization of spec processor instance

#### setCollnCategory() Method Tests
- **testSetCollnCategory**: Test setting valid collection category
- **testSetCollnCategoryWithNull**: Test null collection category handling
- **testSetCollnCategoryWithDifferentCategories**: Test multiple category changes

#### process() Method Tests
- **testProcessWithNullSpec**: Test null BACSpec handling
- **testProcessWithValidSpec**: Test valid BACSpec processing
- **testProcessAddsToSpecLists**: Test spec list population
- **testProcessWithNullSpecLists**: Test null list parameters (expected exception)
- **testProcessWithNullSpecList**: Test null spec list only (expected exception)
- **testProcessWithNullRawSpecList**: Test null raw spec list only (expected exception)
- **testProcessMultipleInvocations**: Test consistency across multiple calls
- **testProcessWithEmptySpecLists**: Test empty list handling
- **testProcessThreadSafety**: Test thread safety with rapid invocations

#### convertJaxbToCollectionSpec() Method Tests
- **testConvertJaxbToCollectionSpecWithNull**: Test null BACSpec handling
- **testConvertJaxbToCollectionSpecWithValidSpec**:  Test valid BACSpec conversion
- **testConvertJaxbToCollectionSpecMultipleInvocations**: Test consistency across multiple calls
- **testConvertJaxbToCollectionSpecReturnsCorrectCategory**: Test correct category assignment

#### convertJaxbToRawCollectionSpec() Method Tests
- **testConvertJaxbToRawCollectionSpecWithNull**: Test null BACSpec handling
- **testConvertJaxbToRawCollectionSpecWithValidSpec**: Test valid BACSpec conversion
- **testConvertJaxbToRawCollectionSpecMultipleInvocations**: Test consistency across multiple calls
- **testConvertJaxbToRawCollectionSpecReturnsCorrectCategory**: Test correct category assignment

#### Interface Implementation Tests
- **testImplementsInterface**: Verify proper BACSpecProcessor interface implementation

### Protected Helper Methods

When present in the spec processor, test helper methods that:  
- Transform JAXB objects to internal specifications
- Validate collection categories and assignments
- Handle spec list manipulation and population
- Process specific object type requirements

### Code Pattern to Follow

#### Standard Test Method Pattern:  
```java
/**
 * Test [method description and expected behavior]
 */
@Test
public void test[MethodName][Scenario]() throws WTException {
    // Arrange
    [Setup test data - BACSpec, lists, categories]
    
    // Act
    [Execute method under test]
    
    // Assert
    Assert.assertNotNull("Result should not be null", result);
    [Additional assertions for expected behavior]
}
```

#### Exception Test Pattern:
```java
@Test(expected = NullPointerException.class)
public void testProcessWithNull[Parameter]() throws WTException {
    specProcessor.process(bacSpec, [null parameter], [valid parameter]);
}
```

#### Category Setting Pattern:
```java
specProcessor.setCollnCategory(CollectionCategory.{OBJECT_TYPE});
```

#### List Size Validation Pattern:
```java
int initialSize = specList.size();
specProcessor.process(bacSpec, specList, rawSpecList);
Assert.assertTrue("List should have entries", specList.size() >= initialSize);
```

#### Conversion Test Pattern:
```java
BAC[Type]CollectionSpec result = specProcessor.convert[Method](bacSpec);
Assert.assertNotNull("Result should not be null", result);
Assert.assertEquals("Category should be {OBJECT_TYPE}", 
                   CollectionCategory.{OBJECT_TYPE}, result.getCollectionCategory());
```

## Critical Rules

### 1. Null Safety
- Handle null BACSpec gracefully in conversion methods (return null)
- Throw NullPointerException for null list parameters in process() method
- Handle null collection category appropriately in setCollnCategory()
- Validate parameters before processing

### 2. List Management
- Populate provided lists rather than creating new ones
- Handle empty lists without errors
- Support multiple invocations that may grow lists
- Maintain list integrity throughout processing

### 3. Collection Category Handling
- Set correct CollectionCategory enum value for object type
- Allow category changes through multiple setCollnCategory() calls
- Ensure converted specs have correct category assignments
- Validate category consistency across conversions

### 4. Conversion Consistency
- Return new instances for each conversion call (don't reuse)
- Maintain consistent behavior across multiple invocations
- Handle JAXB object processing without modifying source
- Ensure thread safety for concurrent processing

## Logging Guidelines

### Test Documentation
- Include comprehensive JavaDoc comments for test classes
- Document the purpose of JAXB to collection spec conversion
- Explain expected behavior for each conversion scenario
- Note any object-specific processing requirements

### Assertion Messages
- Provide clear assertion messages that explain expected behavior
- Use consistent message format:   "Expected behavior description"
- Example: `Assert.assertNotNull("Result should not be null", result);`
- Include context about which specs or lists are being validated

### Test Method Naming
- Use descriptive names that explain the test scenario and expected outcome
- Follow pattern: `test[MethodName][Condition][ExpectedResult]`
- Include parameter states in method names (WithNull, WithValid, etc.)
- Example: `testConvertJaxbToCollectionSpecWithValidSpec`

## Dependencies and Import

### Required Test Framework Imports
```java
import org.junit.Assert;
import org. junit.Before;
import org.junit.Test;
```

### Java Collections Imports
```java
import java.util.ArrayList;
```

### BAC Framework Imports
```java
import com.ptc.windchill. bac.BACCollectionSpec;
import com.ptc.windchill.bac.BACRawCollectionSpec;
import com.ptc. windchill.bac.CollectionCategory;
import com.ptc.windchill.bac.specfile.jaxb.BACSpec;
```

### Windchill Core Imports
```java
import wt.util.WTException;
```

## Import Statements

### Standard Import Order:  
1. Java standard library imports (java.util. *)
2. JUnit framework imports
3. BAC framework imports
4. Windchill core framework imports
5. Spec processor class import (the class being tested)

### Example Import Block:
```java
import java.util.ArrayList;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import com.ptc.windchill.bac.BACCollectionSpec;
import com.ptc.windchill.bac.BACRawCollectionSpec;
import com.ptc. windchill.bac.CollectionCategory;
import com.ptc.windchill.bac.specfile.jaxb. BACSpec;

import wt.util.WTException;
```

## Validation Checklist

### Before Test Generation:  
- [ ] Identify correct CollectionCategory enum value for object type
- [ ] Verify spec processor class exists and implements BACSpecProcessor interface
- [ ] Confirm BACSpec, BACCollectionSpec, and BACRawCollectionSpec availability
- [ ] Check for any custom JAXB processing logic

### After Test Generation:
- [ ] Constructor test validates proper initialization
- [ ] All core methods have comprehensive test coverage
- [ ] Null parameter handling tested with appropriate expected exceptions
- [ ] Valid parameter scenarios covered for all methods
- [ ] List population and manipulation tested thoroughly
- [ ] Category setting and validation tested with multiple scenarios
- [ ] Interface implementation verified

### Code Quality Checks:
- [ ] All imports are present and correctly ordered
- [ ] JavaDoc comments are comprehensive and accurate
- [ ] setUp() method properly initializes all test fixtures
- [ ] WTException is properly declared in method signatures
- [ ] Test independence is maintained (fresh objects for each test)
- [ ] Consistent assertion message format used
- [ ] Proper exception declarations in test annotations

### JAXB Conversion Testing Coverage:
- [ ] Null BACSpec handling returns null for conversion methods
- [ ] Valid BACSpec produces non-null collection specs
- [ ] Converted specs have correct CollectionCategory assignment
- [ ] Multiple conversions produce separate instances
- [ ] Conversion consistency across multiple invocations

### List Processing Testing Coverage:
- [ ] Null list parameters throw NullPointerException in process()
- [ ] Empty lists handled without errors
- [ ] List population verified through size checks
- [ ] Multiple process() calls may grow lists appropriately
- [ ] List integrity maintained throughout processing

### Collection Category Testing Coverage:
- [ ] Valid category setting works without exceptions
- [ ] Null category setting handled gracefully
- [ ] Multiple category changes supported
- [ ] Category consistency in converted specs validated
- [ ] Correct category enum value used for object type

### Thread Safety and Performance:
- [ ] Multiple rapid invocations handled safely
- [ ] Thread safety considerations for concurrent processing
- [ ] Performance with multiple conversions tested
- [ ] Memory usage considerations for list operations
- [ ] Consistent behavior across rapid successive calls

### Interface Implementation Validation:
- [ ] BACSpecProcessor interface properly implemented
- [ ] All required interface methods accessible
- [ ] Interface contract compliance verified
- [ ] Method signatures match interface requirements

### Exception Handling Validation:
- [ ] NullPointerException properly thrown for null lists
- [ ] WTException properly handled in process() method
- [ ] Graceful null handling for optional parameters
- [ ] Expected exception annotations used correctly
- [ ] Exception scenarios documented and tested appropriately