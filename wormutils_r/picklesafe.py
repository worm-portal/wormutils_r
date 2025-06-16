import pandas as pd
import pickle
from io import BytesIO
import dill
from rpy2.rinterface_lib.embedded import RRuntimeError


def make_dataframe_pickle_safe(df, messages=False):
    """
    Extract DataFrame data cell-by-cell and rebuild to make it pickle-safe.
    This bypasses pandas internals that might contain unpicklable references.
    """
    try:
        if messages:
            print(f"Converting DataFrame {df.shape} to pickle-safe format...")
        
        # Extract basic components
        data = []
        columns = [str(col) for col in df.columns]
        index = [str(idx) for idx in df.index]
        
        # Extract data row by row to avoid internal references
        for i in range(len(df)):
            row = []
            for j in range(len(df.columns)):
                try:
                    cell_value = df.iloc[i, j]
                    if pd.isna(cell_value):
                        row.append(None)
                    elif isinstance(cell_value, (int, float, str, bool)):
                        row.append(cell_value)
                    else:
                        row.append(str(cell_value))
                except:
                    row.append(None)
            data.append(row)
        
        # Create new DataFrame from scratch
        new_df = pd.DataFrame(data, index=index, columns=columns)
        
        # Test if it's actually pickle-safe
        buffer = BytesIO()
        pickle.dump(new_df, buffer, protocol=pickle.HIGHEST_PROTOCOL)
        buffer.seek(0)
        pickle.load(buffer)
        
        if messages:
            print(f"✅ Successfully converted to pickle-safe DataFrame")
            
        return new_df
        
    except Exception as e:
        self.err_handler.raise_exception(f"❌ Dataframe conversion to pickle-safe failed: {e}")
        raise
        

def safe_pickle_test(obj):
    """Test pickling while catching R runtime errors"""
    try:
        return dill.pickles(obj)
    except RRuntimeError as e:
        print(f"R Runtime Error during pickle test: {e}")
        return False
    except Exception as e:
        print(f"Other error during pickle test: {e}")
        return False

    
def find_problematic_pickle_parts(obj, path="root", visited=None):
    if visited is None:
        visited = set()
    
    if id(obj) in visited:
        return []
    visited.add(id(obj))
    
    problematic = []
    
    # Test this object with R error protection
    try:
        if not safe_pickle_test(obj):
            problematic.append(path)
            # Still try to recurse to find the specific problem
    except Exception as e:
        problematic.append(f"{path} (error: {e})")
        return problematic  # Don't recurse if we can't even test it
    
    # Continue recursion...
    if hasattr(obj, '__dict__'):
        for attr_name, attr_value in obj.__dict__.items():
            attr_path = f"{path}.{attr_name}"
            try:
                problematic.extend(find_problematic_pickle_parts(attr_value, attr_path, visited))
            except RRuntimeError:
                problematic.append(f"{attr_path} (R runtime error during analysis)")
            except Exception as e:
                problematic.append(f"{attr_path} (error: {e})")
    
    return problematic

### usage
# find_problematic_pickle_parts(speciation)