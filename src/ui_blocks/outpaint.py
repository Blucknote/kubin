from io import BytesIO
import gradio as gr
from ui_blocks.shared.ui_shared import SharedUI
from shared import params

def outpaint_gallery_select(evt: gr.SelectData):
  return [evt.index, f'Selected image index: {evt.index}']

def outpaint_ui(generate_fn, shared: SharedUI, tabs):
  selected_outpaint_image_index = gr.State(None) # type: ignore
  augmentations = shared.create_ext_augment_blocks('outpaint')

  with gr.Row() as outpaint_block:
    with gr.Column(scale=2):
      with gr.Row():
        with gr.Column(scale=1):
          shared.input_outpaint_image.render()
          infer_size = gr.Checkbox(True, label='Infer image size from mask input')

        with gr.Column(scale=1):
          manual_control = gr.Checkbox(True, label='Expansion offset')
          offset_top = gr.Slider(1, 1024, 0, step=params.image_height_step, label='Top', interactive=True)
          with gr.Row():
            offset_left = gr.Slider(0, 1024, 0, step=params.image_width_step, label='Left', interactive=True)
            offset_right = gr.Slider(0, 1024, 0, step=params.image_width_step, label='Right', interactive=True)
          offset_bottom = gr.Slider(0, 1024, 0, step=params.image_height_step, label='Bottom', interactive=True)
        
          manual_control.change(
            fn=lambda x: [gr.update(interactive=x), gr.update(interactive=x), gr.update(interactive=x), gr.update(interactive=x)],
            inputs=[manual_control], outputs=[offset_top, offset_left, offset_right, offset_bottom]
          ) 
 
      with gr.Column():
        prompt = gr.Textbox('', placeholder='', label='Prompt')
        negative_prompt = gr.Textbox('', placeholder='', label='Negative prompt')
        
      with gr.Accordion('Advanced params', open=True):
        with gr.Row():
          steps = gr.Slider(1, 200, 100, step=1, label='Steps')
          guidance_scale = gr.Slider(1, 30, 10, step=1, label='Guidance scale')
        with gr.Row():
          batch_count = gr.Slider(1, 16, 4, step=1, label='Batch count')
          batch_size = gr.Slider(1, 16, 1, step=1, label='Batch size')
        with gr.Row():
          width = gr.Slider(params.image_width_min, params.image_width_max, params.image_width_default, step=params.image_width_step, label='Width', interactive=False)
          height = gr.Slider(params.image_height_min, params.image_height_max, params.image_height_default, step=params.image_height_step, label='Height', interactive=False)
        with gr.Row():
          sampler = gr.Radio(['ddim_sampler', 'p_sampler', 'plms_sampler'], value='p_sampler', label='Sampler')
          seed = gr.Number(-1, label='Seed', precision=0)
        with gr.Row():
          prior_scale = gr.Slider(1, 100, 4, step=1, label='Prior scale')
          prior_steps = gr.Slider(1, 100, 5, step=1, label='Prior steps')
          negative_prior_prompt = gr.Textbox('', label='Negative prior prompt')

      infer_size.change(
        fn=lambda x: [gr.update(interactive=not x), gr.update(interactive=not x)],
        inputs=[infer_size], outputs=[width, height]
      ) 

      augmentations['ui']()

    with gr.Column(scale=1):
      generate_outpaint= gr.Button('Generate', variant='primary')
      outpaint_output = gr.Gallery(label='Generated Images').style(grid=2, preview=True)
      selected_image_info = gr.HTML(value='', elem_classes=['block-info'])
      outpaint_output.select(fn=outpaint_gallery_select, outputs=[selected_outpaint_image_index, selected_image_info], show_progress=False)

      shared.create_base_send_targets(outpaint_output, selected_outpaint_image_index, tabs)
      shared.create_ext_send_targets(outpaint_output, selected_outpaint_image_index, tabs)
       
      def generate(image, prompt, negative_prompt, steps, batch_count, batch_size, guidance_scale, w, h, sampler, prior_cf_scale, prior_steps, negative_prior_prompt, input_seed, manual_size, offset_top, offset_right, offset_bottom, offset_left, infer_size, *injections):
        params = {
          'image': image,
          'prompt': prompt,
          'negative_decoder_prompt': negative_prompt,
          'num_steps': steps,
          'batch_count': batch_count,
          'batch_size': batch_size,
          'guidance_scale': guidance_scale,
          'w': w,
          'h': h,
          'sampler': sampler,
          'prior_cf_scale': prior_cf_scale,
          'prior_steps': prior_steps,
          'negative_prior_prompt': negative_prior_prompt,
          'input_seed': input_seed,
          'offset': None if not manual_size else (offset_top, offset_right, offset_bottom, offset_left),
          'infer_size': infer_size
        }

        params = augmentations['exec'](params, injections)
        return generate_fn(params)
    
    generate_outpaint.click(generate, inputs=[
      shared.input_outpaint_image, prompt, negative_prompt, steps, batch_count, batch_size, guidance_scale, width, height, sampler, prior_scale, prior_steps, negative_prior_prompt, seed,
      manual_control,
      offset_top,
      offset_right,
      offset_bottom,
      offset_left,
      infer_size 
    ] + augmentations['injections'],
    outputs=outpaint_output)

  return outpaint_block
